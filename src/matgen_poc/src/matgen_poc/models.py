"""
結晶構造生成モデル（VAE）
"""
import torch
import torch.nn as nn
from typing import Tuple


class CrystalVAE(nn.Module):
    """
    結晶構造生成用VAE（簡易版）
    
    Note: 実用的には torch_geometric を使った Graph VAE が必要
          PoCでは組成ベクトルから始める簡易版
    """
    
    def __init__(
        self, 
        input_dim: int = 100,
        latent_dim: int = 256,
        encoder_layers: list = [512, 256],
        decoder_layers: list = [256, 512]
    ):
        super().__init__()
        
        # Encoder
        encoder_arch = [input_dim] + encoder_layers
        encoder_modules = []
        for i in range(len(encoder_arch) - 1):
            encoder_modules.extend([
                nn.Linear(encoder_arch[i], encoder_arch[i+1]),
                nn.ReLU(),
                nn.BatchNorm1d(encoder_arch[i+1])
            ])
        self.encoder = nn.Sequential(*encoder_modules)
        
        # Latent space
        self.fc_mu = nn.Linear(encoder_layers[-1], latent_dim)
        self.fc_logvar = nn.Linear(encoder_layers[-1], latent_dim)
        
        # Decoder
        decoder_arch = [latent_dim] + decoder_layers + [input_dim]
        decoder_modules = []
        for i in range(len(decoder_arch) - 1):
            decoder_modules.append(nn.Linear(decoder_arch[i], decoder_arch[i+1]))
            if i < len(decoder_arch) - 2:
                decoder_modules.extend([nn.ReLU(), nn.BatchNorm1d(decoder_arch[i+1])])
        self.decoder = nn.Sequential(*decoder_modules)
    
    def encode(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Encode input to latent distribution"""
        h = self.encoder(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar
    
    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        """Reparameterization trick"""
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """Decode latent vector to output"""
        return self.decoder(z)
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass"""
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        return x_recon, mu, logvar
    
    def sample(self, num_samples: int, device: str = "cpu") -> torch.Tensor:
        """Generate new samples from prior"""
        z = torch.randn(num_samples, self.fc_mu.out_features).to(device)
        return self.decode(z)


def vae_loss(
    x: torch.Tensor, 
    x_recon: torch.Tensor, 
    mu: torch.Tensor, 
    logvar: torch.Tensor,
    beta: float = 1.0
) -> torch.Tensor:
    """
    VAE loss = Reconstruction loss + KL divergence
    
    Args:
        x: 元データ
        x_recon: 再構成データ
        mu: 平均
        logvar: 対数分散
        beta: KL項の重み
    """
    # Reconstruction loss (MSE)
    recon_loss = nn.functional.mse_loss(x_recon, x, reduction='sum')
    
    # KL divergence
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    
    return recon_loss + beta * kl_loss
