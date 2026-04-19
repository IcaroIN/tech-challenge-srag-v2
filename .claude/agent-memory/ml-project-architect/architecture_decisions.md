---
name: Architecture Decisions
description: Estrutura de módulos, padrões adotados, artefatos gerados e convenções do projeto
type: project
---

**Why:** Documentar decisões tomadas para manter consistência em futuras mudanças.

**How to apply:** Ao propor refatorações ou novas funcionalidades, respeitar essas convenções já estabelecidas.

## Estrutura de módulos src/

- `load_data.py` — carregamento do CSV (sep=";", encoding=latin-1), inspeção, resumo do target
- `preprocessing.py` — pipeline completo: filtro → target binário → feature selection → imputation → label encoding → scaler → split
- `modeling.py` — definição dos 4 modelos + GridSearchCV + persistência
- `evaluation.py` — métricas, visualizações, SHAP. matplotlib backend="Agg" para execução sem display

## Artefatos e caminhos

- Dados processados: `data/processed/` — X_train/val/test.parquet, y_train/val/test.parquet, scaler.pkl, encoders.pkl
- Modelos: `results/models/{nome_modelo}.pkl`
- Figuras: `results/figures/*.png`
- Dados brutos: `data/raw/INFLUD24-26-06-2025.csv` (não versionado no git)

## Convenções de nomenclatura

- Funções em português (carregar_dataset, filtrar_registros_validos, etc.)
- Constantes em MAIÚSCULAS (FEATURES, TARGET, PROCESSED_DIR, RANDOM_STATE)
- random_state=42 em todos os modelos e splits

## Controle de paralelismo

- SRAG_GRID_N_JOBS env var controla n_jobs do GridSearchCV (default=1 para evitar RAM overflow)
- Quando GRID_N_JOBS > 1, n_jobs dos estimadores internos é forçado para 1 (evitar paralelismo aninhado)

## Feature engineering

- 35 features selecionadas manualmente em grupos: DEMOGRAFICAS (7), SINTOMAS (12), COMORBIDADES (12), INTERNACAO (4), VACINA (2)
- FEATURES_INTERNACAO inclui UTI e SUPORT_VEN — atenção: essas features são coletadas durante a internação e podem ser post-hoc (risco clínico de data leakage conceitual, a discutir)
