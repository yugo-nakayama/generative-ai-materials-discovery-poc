"""
Materials Project データの前処理・クリーニング
"""
import json
from typing import List, Dict, Any
from pymatgen.core import Structure, Composition


def load_mp_data(filepath: str) -> List[Dict[str, Any]]:
    """JSONからMaterials Projectデータを読み込み"""
    with open(filepath, 'r') as f:
        return json.load(f)


def filter_stable_materials(
    data: List[Dict], 
    max_energy_above_hull: float = 0.1
) -> List[Dict]:
    """
    安定な材料のみをフィルタ
    
    Args:
        data: Materials Projectデータ
        max_energy_above_hull: 許容する最大エネルギー (eV/atom)
    
    Returns:
        フィルタ後のデータ
    """
    filtered = [
        item for item in data 
        if item.get('energy_above_hull', float('inf')) <= max_energy_above_hull
    ]
    print(f"安定性フィルタ: {len(data)} → {len(filtered)} 件")
    return filtered


def extract_features(data: List[Dict]) -> List[Dict]:
    """
    構造から特徴量を抽出（後でGNN用に拡張）
    
    Args:
        data: Materials Projectデータ
    
    Returns:
        特徴量を追加したデータ
    """
    for item in data:
        structure = Structure.from_dict(item['structure'])
        composition = structure.composition
        
        # 基本特徴
        item['num_sites'] = len(structure)
        item['volume'] = structure.volume
        item['density'] = structure.density
        item['num_elements'] = len(composition.elements)
        
    return data


def split_dataset(
    data: List[Dict], 
    train_ratio: float = 0.8, 
    seed: int = 42
) -> tuple:
    """
    データセットをtrain/testに分割
    
    Args:
        data: 全データ
        train_ratio: 学習データの割合
        seed: ランダムシード
    
    Returns:
        (train_data, test_data)
    """
    import random
    random.seed(seed)
    random.shuffle(data)
    
    split_idx = int(len(data) * train_ratio)
    train_data = data[:split_idx]
    test_data = data[split_idx:]
    
    print(f"データ分割: train={len(train_data)}, test={len(test_data)}")
    return train_data, test_data


if __name__ == "__main__":
    # 動作確認用
    data = load_mp_data("data/raw/mp_battery_materials.json")
    print(f"読み込み: {len(data)} 件")
    
    filtered = filter_stable_materials(data, max_energy_above_hull=0.1)
    enhanced = extract_features(filtered)
    train, test = split_dataset(enhanced)
    
    print("前処理完了")
