Tech Challenge Fase 1 — Classificação de SRAG (SIVEP-Gripe)
Objetivo

Construir um sistema de apoio à decisão clínica capaz de prever o desfecho de pacientes com Síndrome Respiratória Aguda Grave (SRAG), utilizando:

Dados tabulares clínicos (SIVEP-Gripe)
Validação complementar por imagens (radiografias torácicas)

O foco é compreender o comportamento de modelos de Machine Learning e Deep Learning aplicados à saúde, explorando tanto dados estruturados quanto não estruturados.

Dataset
1. Dados Tabulares — SIVEP-Gripe
Fonte: OpenDataSUS
Arquivo: INFLUD24-26-06-2025.csv
Registros: ~268 mil
Variáveis: 194

Variável alvo:

EVOLUCAO
1 = Cura
2 = Óbito

Transformação aplicada:

0 = Cura
1 = Óbito

Coloque o arquivo em:

data/raw/
2. Dados de Imagem — Radiografias Torácicas
Fonte: COVID-19 Radiography Database (Kaggle)
Download automático via kagglehub

Classes utilizadas:

COVID
Normal
Lung_Opacity
Viral Pneumonia

Observação:

Nesta fase, o modelo de imagem é treinado do zero (sem transfer learning)
Foi aplicada data augmentation para melhorar a generalização
Estrutura do Projeto
tech_challenge_srag/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_modeling.ipynb
│   ├── 04_evaluation_interpretability.ipynb
│   └── 05_image_validation.ipynb
├── src/
│   ├── tabular/
│   │   ├── load_data.py
│   │   ├── preprocessing.py
│   │   ├── modeling.py
│   │   └── evaluation.py
│   │
│   └── image/
│       ├── image_data.py
│       ├── image_preprocessing.py
│       ├── image_model.py
│       └── image_evaluation.py
│
├── docs/
│   └── documentacao_tecnica.docx
├── results/
│   ├── figures/
│   └── models/
├── run_pipeline.py
├── requirements.txt
└── Dockerfile
Requisitos

Utilizar:

Python 3.11 ou 3.12

Evitar versões muito recentes (ex: 3.14), pois podem causar falhas na instalação de dependências científicas.

Instalação e Execução Local
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Adicionar dataset
colocar INFLUD24-26-06-2025.csv em data/raw/

# Executar pipeline
python run_pipeline.py

# Executar notebooks
jupyter notebook notebooks/
Execução com Docker
docker build -t tech-challenge-srag .
docker run -p 8888:8888 -v $(pwd)/data:/app/data tech-challenge-srag
Fluxo dos Notebooks
Notebook	Descrição
01_exploratory_data_analysis	Análise exploratória dos dados
02_preprocessing	Limpeza e preparação dos dados
03_modeling	Treinamento dos modelos tabulares
04_evaluation_interpretability	Avaliação e interpretabilidade (SHAP)
05_image_validation	Classificação de imagens com CNN
Modelos Utilizados
Dados Tabulares
Regressão Logística
Árvore de Decisão
Random Forest
XGBoost
Dados de Imagem
CNN construída do zero (Keras)
Data augmentation aplicado
Métricas de Avaliação
Tabular
Accuracy
Precision
Recall
F1-score
ROC-AUC
Imagem
Accuracy
Precision
Recall
F1-score
Matriz de confusão
Principais Observações Técnicas
Modelos simples de CNN apresentaram dificuldade inicial de generalização
Houve tendência de colapso para uma única classe em cenários com poucos dados
A aplicação de data augmentation foi necessária para melhorar o desempenho
O projeto demonstra a diferença de comportamento entre modelos tabulares e de visão computacional
Possíveis Evoluções
Implementação de modelo multimodal (imagem + dados clínicos)
Uso de transfer learning (MobileNet, EfficientNet)
Deploy como API
Monitoramento de modelo (MLOps)
Conclusão

O projeto demonstra, na prática, o desenvolvimento de um pipeline completo de Machine Learning aplicado à saúde, desde a análise exploratória até a validação com imagens médicas, evidenciando desafios reais como:

qualidade de dados
generalização de modelos
diferença entre abordagens tabulares e visuais