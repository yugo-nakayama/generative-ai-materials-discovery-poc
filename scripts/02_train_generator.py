#!/usr/bin/env python3
"""
結晶構造生成モデルの学習スクリプト
"""
import os
import json
import yaml
import argparse
import torch
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from pathlib import Path

# 自作モジュール（後で実装）
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from matgen_poc.models import CrystalVAE, vae_loss


class CompositionDataset(Dataset):
    """
    組成ベクトルデータセット（簡易版）
    
    Note: 実用的にはグラフ構造を扱う必要あり
    """
    
    def __init__(self, data_path: str, max_elements: int = 100):
        with open(data_path, 'r') as f:
            self.data = json.load(f)
        
        self.max_elements = max_elements
        self.vectors = self._featurize()
    
    def _featurize(self):
        """組成を固定長ベクトルに変換（簡易版）"""
        vectors = []
        for item in self.data:
            # ダミー特徴量（実際は pymatgen の Composition.fractional_composition 等を使う）
            vec = np.random.randn(self.max_elements)  # TODO: 実装
            vectors.append(vec)
        return np.array(vectors, dtype=np.float32)
    
    def __len__(self):
        return len(self.vectors)
    
    def __getitem__(self, idx):
        return torch.from_numpy(self.vectors[idx])


def train_epoch(model, dataloader, optimizer, device, beta=1.0):
    """1エポックの学習"""
    model.train()
    total_loss = 0
    
    for batch in dataloader:
        batch = batch.to(device)
        
        # Forward
        x_recon, mu, logvar = model(batch)
        loss = vae_loss(batch, x_recon, mu, logvar, beta)
        
        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(dataloader.dataset)


def main(config_path: str):
    # 設定読み込み
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    device = torch.device(config['device'] if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # データセット
    print("Loading data...")
    train_dataset = CompositionDataset(config['data']['train_data'])
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=True
    )
    
    # モデル
    print("Initializing model...")
    model = CrystalVAE(
        input_dim=train_dataset.max_elements,
        latent_dim=config['model']['latent_dim'],
        encoder_layers=config['model']['encoder_layers'],
        decoder_layers=config['model']['decoder_layers']
    ).to(device)
    
    optimizer = optim.Adam(model.parameters(), lr=config['training']['learning_rate'])
    
    # 学習
    print("Training...")
    os.makedirs(config['output']['model_dir'], exist_ok=True)
    
    for epoch in range(config['training']['epochs']):
        loss = train_epoch(model, train_loader, optimizer, device)
        print(f"Epoch {epoch+1}/{config['training']['epochs']}, Loss: {loss:.4f}")
        
        # チェックポイント保存
        if (epoch + 1) % config['output']['checkpoint_every'] == 0:
            checkpoint_path = os.path.join(
                config['output']['model_dir'],
                f"checkpoint_epoch_{epoch+1}.pt"
            )
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
            }, checkpoint_path)
            print(f"Saved checkpoint: {checkpoint_path}")
    
    # 最終モデル保存
    final_path = os.path.join(config['output']['model_dir'], "final_model.pt")
    torch.save(model.state_dict(), final_path)
    print(f"Training complete. Model saved to {final_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/train_generator.yaml")
    args = parser.parse_args()
    
    main(args.config)
