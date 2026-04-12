# Tech Challenge Fase 1 — Classificação de SRAG (SIVEP-Gripe)

## Objetivo

Construir um modelo de Machine Learning para prever o desfecho clínico (cura ou óbito) de pacientes com Síndrome Respiratória Aguda Grave (SRAG) hospitalizados, utilizando dados do sistema SIVEP-Gripe do Ministério da Saúde.

## Dataset

**SIVEP-Gripe — INFLUD24** (~268 mil registros, 194 variáveis)

- Fonte: [OpenDataSUS](https://opendatasus.saude.gov.br/dataset/srag-2021-a-2024)
- Arquivo: `INFLUD24-26-06-2025.csv` (separador `;`, encoding `latin-1`)
- Variável alvo: `EVOLUCAO` (1 = Cura, 2 = Óbito → binário: 0/1)

Coloque o arquivo CSV em `data/raw/` antes de executar os notebooks.

## Estrutura do Projeto

```
tech_challenge_srag/
├── data/
│   ├── raw/              # Dataset original
│   └── processed/        # Dados pré-processados
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_modeling.ipynb
│   └── 04_evaluation_interpretability.ipynb
├── src/
│   ├── load_data.py
│   ├── preprocessing.py
│   ├── modeling.py
│   └── evaluation.py
├── docs/
│   └── documentacao_tecnica.docx
├── results/
│   ├── figures/
│   └── models/
├── run_pipeline.py
├── requirements.txt
└── Dockerfile
```

## Instalação e Execução Local

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Copiar dataset
cp /caminho/para/INFLUD24-26-06-2025.csv data/raw/

# Executar pipeline completo
python run_pipeline.py

# Ou abrir notebooks individualmente
jupyter notebook notebooks/
```

## Execução via Docker

```bash
docker build -t tech-challenge-srag .
docker run -p 8888:8888 -v $(pwd)/data:/app/data tech-challenge-srag
```

## Fluxo dos Notebooks

| Notebook | Descrição |
|----------|-----------|
| `01_exploratory_data_analysis` | Carregamento, estatísticas descritivas, visualizações |
| `02_preprocessing` | Limpeza, feature engineering, correlação, split |
| `03_modeling` | Treinamento de 4 modelos com tuning |
| `04_evaluation_interpretability` | Métricas, ROC, SHAP, feature importance |

## Modelos Utilizados

- Regressão Logística (baseline)
- Árvore de Decisão
- Random Forest
- XGBoost (Gradient Boosting)

## Métricas de Avaliação

- Accuracy, Precision, Recall, F1-score
- ROC-AUC
- Matriz de confusão
