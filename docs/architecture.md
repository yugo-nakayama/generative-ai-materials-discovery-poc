# アーキテクチャ設計

## システム全体フロー

graph TD
A[Materials Project API] -->|データ取得| B[前処理・EDA]
B --> C[学習データセット]
C --> D[生成モデル学習]
C --> E[予測モデル学習]
D --> F[条件付き構造生成]
F --> G[候補材料リスト]
E --> H[物性予測]
G --> H
H --> I[フィルタリング]
I --> J[上位N件抽出]
J --> K[DFT検証]
K --> L[専門家評価]
L --> M[最終候補材料]


## モジュール構成

### 1. データ取得・前処理（`src/matgen_poc/data_mp.py`）
- Materials Project APIから電池材料データを取得
- 結晶構造、組成、物性値（伝導度、安定性）を抽出
- 欠損処理、外れ値除去、正規化

### 2. 構造生成（`src/matgen_poc/generate.py`）
- **入力**：目的特性（組成範囲、伝導度下限、安定性条件）
- **出力**：CIF形式の結晶構造候補
- **手法**：拡散モデル or VAE

### 3. 物性予測（`src/matgen_poc/predictor.py`）
- **入力**：生成された結晶構造（CIF）
- **出力**：イオン伝導度、形成エネルギー、信頼区間
- **モデル**：グラフニューラルネット（SchNet/MEGNet）

### 4. フィルタリング（`src/matgen_poc/validate_structure.py`）
- 化学的妥当性チェック（組成バランス、原子距離）
- 安定性フィルタ（energy above hull < 閾値）
- 物性条件フィルタ（伝導度 > 目標値）

### 5. 評価（`src/matgen_poc/metrics.py`）
- 生成品質（妥当性、多様性）
- 予測精度（MAE, R²）
- 探索効率（時間、候補数）

## データフォーマット

### Materials Project取得データ
