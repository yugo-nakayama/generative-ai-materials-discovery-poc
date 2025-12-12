#!/usr/bin/env python3
"""
Materials Projectから電池材料データを取得するスクリプト
"""
import os
import json
import argparse
from mp_api.client import MPRester

def main(output_path: str, max_results: int = 1000):
    api_key = os.getenv("MP_API_KEY")
    if not api_key:
        raise ValueError("MP_API_KEY環境変数が設定されていません")
    
    print(f"Materials Project APIに接続中...")
    with MPRester(api_key) as mpr:
        # 電池材料の検索（例：Li含有化合物）
        # TODO: 検索条件を詳細化
        docs = mpr.materials.summary.search(
            elements=["Li"],
            num_elements=(2, 5),
            fields=["material_id", "formula_pretty", "structure", "energy_above_hull"],
        )
        
        results = []
        for doc in docs[:max_results]:
            results.append({
                "material_id": doc.material_id,
                "formula": doc.formula_pretty,
                "structure": doc.structure.as_dict(),
                "energy_above_hull": doc.energy_above_hull,
            })
        
        print(f"取得件数: {len(results)}")
        
        # 保存
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"データを保存しました: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/mp_battery_materials.json")
    parser.add_argument("--max-results", type=int, default=1000)
    args = parser.parse_args()
    
    main(args.output, args.max_results)

# 1. データ取得（APIキー設定済み前提）
# python scripts/01_download_mp.py --output data/raw/mp_battery_materials.json --max-results 1000

