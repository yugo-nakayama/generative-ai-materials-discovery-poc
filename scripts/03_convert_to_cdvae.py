#!/usr/bin/env python3
"""
Materials Project データを CDVAE フォーマットに変換
"""
import json
import csv
import os
from pathlib import Path
from pymatgen.core import Structure

def main():
    # 入力データ
    input_path = "data/processed/train.json"
    output_dir = Path("data/cdvae_format")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # データ読み込み
    with open(input_path) as f:
        data = json.load(f)
    
    # CSVファイル作成
    csv_path = output_dir / "train.csv"
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['material_id', 'cif', 'formation_energy_per_atom'])
        
        for item in data[:100]:  # まず100件でテスト
            mat_id = item['material_id']
            
            # 構造をCIF文字列に変換
            try:
                structure = Structure.from_dict(item['structure'])
                cif_str = structure.to(fmt="cif")
                
                # エネルギー（ダミーまたは実データ）
                energy = item.get('energy_above_hull', 0.0)
                
                writer.writerow([mat_id, cif_str, energy])
            except Exception as e:
                print(f"Warning: {mat_id} の変換失敗: {e}")
                continue
    
    print(f"変換完了: {csv_path}")
    print(f"件数: {len(data)} → CSV出力")

if __name__ == "__main__":
    main()
