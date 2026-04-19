# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FIAP Pos-Tech Phase 1 challenge: ML classification model predicting clinical outcome (cure vs death) for hospitalized SRAG (Severe Acute Respiratory Syndrome) patients, using SIVEP-Gripe data from the Brazilian Ministry of Health.

- **Target variable**: `EVOLUCAO` → binary `OBITO` (0=Cure, 1=Death)
- **Dataset**: `INFLUD24-26-06-2025.csv` — ~268k records, 194 columns, semicolon-separated, latin-1 encoding
- **Place dataset at**: `data/raw/INFLUD24-26-06-2025.csv` before running anything

## Setup

Requires **Python 3.11 or 3.12** (avoid 3.13+ due to wheel compatibility issues with numpy/pandas/matplotlib).

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Pipeline

```bash
# Full pipeline (all steps sequentially)
python run_pipeline.py

# Or run notebooks interactively
jupyter notebook notebooks/
```

## Parallelism Note

GridSearchCV runs single-threaded by default to avoid RAM exhaustion from nested parallelism. To speed up on machines with enough memory:

```bash
export SRAG_GRID_N_JOBS=4
python run_pipeline.py
```

## Architecture

The project follows a linear notebook pipeline backed by reusable `src/` modules:

```
Notebook 01 (EDA) → Notebook 02 (Preprocessing) → Notebook 03 (Modeling) → Notebook 04 (Evaluation)
```

### `src/` modules

| Module | Responsibility |
|--------|---------------|
| `load_data.py` | Loads CSV with correct sep/encoding; `carregar_dataset()`, `inspecionar_dataset()`, `resumo_target()` |
| `preprocessing.py` | Full preprocessing pipeline: filter valid outcomes → binary target → feature selection → imputation → label encoding → StandardScaler → 70/15/15 stratified split. Saves parquet splits + scaler/encoder pkl to `data/processed/`. Entry point: `executar_pipeline_preprocessamento()` |
| `modeling.py` | Defines 4 models (LogisticRegression, DecisionTree, RandomForest, XGBoost) with GridSearchCV param grids. All use `class_weight='balanced'`. Entry points: `treinar_todos_modelos()`, `carregar_modelos()` |
| `evaluation.py` | Metrics (accuracy, precision, recall, F1, ROC-AUC), confusion matrices, ROC/PR curves, feature importance, SHAP summary plots. Saves all figures to `results/figures/`. Entry point: `avaliar_todos_modelos()` |

### Data flow

- Raw CSV → `load_data.carregar_dataset()` → `preprocessing.executar_pipeline_preprocessamento()` → parquet splits in `data/processed/`
- Parquet splits → `modeling.treinar_todos_modelos()` → pkl models in `results/models/`
- Loaded models → `evaluation.avaliar_todos_modelos()` → figures in `results/figures/`

### Features used in the model

35 clinical features grouped in `preprocessing.py` as constants:
- `FEATURES_DEMOGRAFICAS` (7): sex, age, pregnancy, race, education, urban/rural zone
- `FEATURES_SINTOMAS` (12): fever, cough, dyspnea, O2 saturation, etc.
- `FEATURES_COMORBIDADES` (12): cardiovascular, diabetes, obesity, etc.
- `FEATURES_INTERNACAO` (4): ICU, ventilatory support, nosocomial
- `FEATURES_VACINA` (2): influenza and COVID-19 vaccination

### Artifacts saved

- `data/processed/X_train.parquet`, `X_val.parquet`, `X_test.parquet` + y counterparts
- `data/processed/scaler.pkl`, `encoders.pkl`
- `results/models/{model_name}.pkl`
- `results/figures/confusion_matrix_*.png`, `roc_curves.png`, `precision_recall_curves.png`, `feature_importance_*.png`, `shap_summary_*.png`
