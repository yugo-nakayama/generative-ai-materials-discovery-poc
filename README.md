# 生成AIによる材料探索PoC

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

生成AIを活用した電池材料(リチウムイオン伝導体・固体電解質)候補の自動生成と物性予測システムのProof of Concept

## 🎯 プロジェクト概要

### 課題定義
従来の材料開発では新材料の候補探索に数ヶ月〜数年を要しており、カーボンニュートラル実現や次世代製品開発に必要な高性能材料の創出が遅延している。本PoCでは生成AIを活用し、目的特性を満たす材料候補の自動生成と探索時間の劇的短縮(従来比1/100)を実現する。

### 技術的目標
- ✅ 生成AIモデルによる特性指定材料候補の自動生成(目標:有効候補10件以上/実行)
- ✅ 生成材料の物性予測精度:MAE 10%以内(DFT計算結果との比較)
- ✅ 探索時間:従来手法比1/100以下(数ヶ月→数時間)
- ✅ 生成材料の化学的妥当性95%以上

### 対象材料
電池材料(リチウムイオン伝導体、固体電解質候補)

## 🏗️ プロジェクト構成

```
.
├── README.md                    # プロジェクト概要
├── docs/                        # ドキュメント
│   ├── proposal.md              # 企画書詳細
│   ├── technical_spec.md        # 技術仕様書
│   ├── milestones.md            # マイルストーン管理
│   └── references.md            # 参考文献・事例
├── data/                        # データセット
│   ├── raw/                     # 生データ
│   ├── processed/               # 前処理済みデータ
│   └── external/                # 外部データソース
├── notebooks/                   # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_evaluation.ipynb
├── src/                         # ソースコード
│   ├── data/                    # データ処理
│   ├── models/                  # モデル定義
│   ├── training/                # 学習パイプライン
│   ├── inference/               # 推論・生成
│   └── evaluation/              # 評価スクリプト
├── configs/                     # 設定ファイル
├── experiments/                 # 実験結果
├── tests/                       # テストコード
├── docker/                      # Docker設定
├── requirements.txt             # Python依存関係
└── setup.py                     # パッケージセットアップ
```

## 📊 成功基準

### 技術KPI
| 指標 | 目標値 | 測定方法 |
|------|--------|----------|
| 生成材料の化学安定性 | 90%以上 | DFT計算による形成エネルギー評価 |
| 物性予測MAE | ≤10% | テストセットでの予測誤差 |
| 生成速度 | 100材料/時間 | GPU環境での実測 |
| 構造的妥当性 | 95%以上 | 結晶構造検証ツールによる判定 |

### ビジネスKPI
| 指標 | 目標値 | 測定根拠 |
|------|--------|----------|
| 候補材料抽出時間 | 従来比1/100 | 実測比較(数ヶ月→数時間) |
| 実験コスト削減率 | 70% | 不要な合成実験の削減数 |
| 専門家評価スコア | 3.5/5.0以上 | 5段階評価アンケート |
| 特許出願可能性 | 1件以上 | 新規材料候補の評価結果 |

## 🛠️ 技術スタック

### データセット
- **Materials Project API**: 150,000以上の無機材料データ(結晶構造、物性値)
- **社内実験データ**: 過去5年分の電池材料評価データ(約500サンプル)
- **文献データ**: 関連論文から抽出した材料-物性ペア(1,000件)

### フレームワーク・ライブラリ
- **生成モデル**: PyTorch, PyTorch Geometric, DiffCSP(拡散モデル)
- **物性予測**: MEGNet, SchNet(グラフNN)
- **材料解析**: Pymatgen, ASE, VESTA
- **DFT計算**: VASP / Quantum Espresso(検証用)
- **実験管理**: MLflow, Weights & Biases

### 計算環境
- **GPU**: NVIDIA A100 40GB × 2基(AWS g5.12xlarge)
- **ストレージ**: 2TB SSD
- **クラウド予算**: 月額15万円(3ヶ月想定)

## 📅 スケジュール (8週間)

| 週 | タスク | 成果物 |
|----|--------|--------|
| 1-2週目 | データ収集・前処理・EDA | クリーニング済みデータセット、統計分析レポート |
| 3-4週目 | 生成モデル実装・学習 | 学習済み生成モデル、学習曲線 |
| 5-6週目 | 物性予測モデル統合・材料生成 | 統合パイプライン、候補材料リスト |
| 7週目 | DFT検証・専門家評価 | 検証レポート、評価スコア |
| 8週目 | 文書化・プレゼン準備 | 最終レポート、説明資料 |

### マイルストーン
- ✨ **Week 2**: データ品質確認会(専門家レビュー)
- ✨ **Week 4**: 生成モデルベースライン確立
- ✨ **Week 6**: 初回材料候補生成完了
- ✨ **Week 8**: PoC成果発表会

## 🚀 クイックスタート

### 環境構築

```bash
# リポジトリクローン
git clone https://github.com/yugo-nakayama/generative-ai-materials-discovery-poc.git
cd generative-ai-materials-discovery-poc

# Docker環境構築
cd docker
docker-compose up -d

# または、ローカル環境
pip install -r requirements.txt
pip install -e .
```

### データ準備

```bash
# Materials Project APIキー設定
export MP_API_KEY="your_api_key_here"

# データダウンロード
python src/data/download_materials_project.py
```

### モデル学習

```bash
# 生成モデル学習
python src/training/train_generative_model.py --config configs/diffusion_model.yaml

# 物性予測モデル学習
python src/training/train_property_predictor.py --config configs/megnet_model.yaml
```

### 材料生成

```bash
# 特性指定材料生成
python src/inference/generate_materials.py \
    --target_conductivity 1e-3 \
    --num_candidates 100 \
    --output experiments/generated_materials.json
```

## 📈 成果物

### コード・リポジトリ
- ✅ 再現可能な実装(Docker環境含む)
- ✅ データ前処理パイプライン
- ✅ 生成モデル学習・推論コード
- ✅ 物性予測モデル
- ✅ 評価スクリプト
- ✅ モデルチェックポイント(Hugging Face Hub公開予定)

### 技術レポート
- 手法説明(モデルアーキテクチャ、ハイパーパラメータ、学習プロセス)
- 結果(定量評価、生成材料の化学的分析)
- 考察(成功要因、失敗事例分析、改善提案)
- ベンチマーク比較(ベイズ最適化、遺伝的アルゴリズム)

### 可視化資料
- 材料空間マップ(t-SNE)
- 物性予測グラフ
- 化学構造図(3D結晶構造)
- 学習曲線

## 🔬 参考文献・事例

- [住友ゴム×NEC: AI材料配合予測](https://www.srigroup.co.jp/newsrelease/2025/sri/2025_088.html)
- [NTTデータ: CO2触媒探索への生成AI適用](https://www.nttdata.com/jp/ja/trends/data-insight/2025/1106/)
- [Microsoft Research: MatterGen](https://www.microsoft.com/en-us/research/blog/mattergen-a-new-paradigm-of-materials-design-with-generative-ai/)
- [MIT: SCIGEN](https://news.mit.edu/2025/new-tool-makes-generative-ai-models-likely-create-breakthrough-materials-0922)

詳細は[docs/references.md](docs/references.md)を参照

## 📝 ライセンス

MIT License

## 👥 コントリビューター

- Yugo NAKAYAMA ([@yugo-nakayama](https://github.com/yugo-nakayama))

## 📧 コンタクト

プロジェクトに関する質問・提案はIssueまたはPull Requestでお願いします。
