---
name: Project Context
description: Contexto geral do projeto — FIAP Pos-Tech Fase 1, dataset, target, tecnologias
type: project
---

Projeto de pós-graduação FIAP Pos-Tech Fase 1: classificação binária de desfecho clínico (cura vs óbito) de pacientes com SRAG (Síndrome Respiratória Aguda Grave), dados SIVEP-Gripe do Ministério da Saúde.

**Why:** Requisito acadêmico da pós-graduação, com entrega esperada no prazo da Fase 1.

**How to apply:** Priorizar reprodutibilidade e documentação para avaliação acadêmica. Manter foco em boas práticas de ML engineering sem over-engineering.

- Dataset: INFLUD24-26-06-2025.csv (~268k registros, 194 colunas, sep=";", encoding=latin-1) — não versionado no git
- Target: EVOLUCAO → binário OBITO (0=Cura, 1=Óbito)
- Python 3.11 ou 3.12 (3.13+ tem problemas de wheel compatibility com numpy/pandas/matplotlib)
- Stack: pandas, scikit-learn, XGBoost, SHAP, matplotlib/seaborn, joblib, pyarrow
- 4 modelos: LogisticRegression, DecisionTree, RandomForest, XGBoost — todos com class_weight='balanced'
- GridSearchCV com StratifiedKFold 5-fold, scoring=f1
- Split estratificado 70/15/15 (treino/validação/teste), random_state=42
- 35 features clínicas selecionadas manualmente (demográficas, sintomas, comorbidades, internação, vacinação)
