---
name: Known Issues
description: Problemas técnicos identificados e status de resolução — atualizado 2026-04-19
type: project
---

Auditoria realizada em 2026-04-19.

**Why:** Identificados durante auditoria completa do código fonte (src/ + notebooks).

**How to apply:** Consultar antes de propor mudanças para não regredir correções já aplicadas.

## RESOLVIDO — Data Leakage no Preprocessing

`preprocessing.py` foi reescrito com a ordem correta: dividir_dados() ocorre ANTES de qualquer fit().
Imputadores, encoders e scaler são fitados apenas em X_train. Testes cobrem esta invariante.

## RESOLVIDO — run_pipeline.py não existia

`run_pipeline.py` foi criado com argparse completo: --no-grid, --no-shap, --nrows, --data.
Makefile tem targets: install, test, run, run-fast, run-quick, lint.

## RESOLVIDO — Sem testes automatizados

`tests/test_preprocessing.py` — 8 testes cobrindo filtro, target, splits, leakage de imputação/encoding/scaler.
`tests/test_modeling.py` — 10 testes cobrindo definir_modelos, scale_pos_weight XGBoost, treinamento e predições.
Total: 18 testes, todos passando (pytest 9.0.3, Python 3.12).

## RESOLVIDO — XGBoost sem balanceamento de classes

XGBClassifier não aceita class_weight='balanced'. Corrigido em 2026-04-19:
- `definir_modelos()` agora aceita `scale_pos_weight: float = 1.0`
- `treinar_todos_modelos()` calcula `n_neg / n_pos` automaticamente e passa ao XGBoost
- Notebook 03 atualizado para calcular e passar scale_pos_weight ao chamar `definir_modelos()`

## RESOLVIDO — Bug typo no notebook 03 (célula de carregamento de dados)

Linha `y_test = pd.read_parquet(PROCESSED / 'X_test.parquet')` (carregava X no lugar de y)
foi removida. A célula agora carrega y_test corretamente apenas uma vez.

## PENDENTE — Configuração hardcoded nos módulos

Paths, RANDOM_STATE, nomes de features e parâmetros estão hardcoded em src/.
Não há configs/ com YAML centralizados. Impacto: baixo para o escopo do desafio FIAP.

## PENDENTE — Modelos salvos sem metadados

Modelos em results/models/*.pkl são salvos sem registro de métricas, data ou hiperparâmetros.
Recomendado: salvar junto um JSON com metadados por modelo. Impacto: médio.

## PENDENTE — Sem CI/CD

Sem GitHub Actions para rodar testes automaticamente em PRs. Impacto: baixo para projeto acadêmico.

## POTENCIAL MELHORIA — Features adicionais identificadas no dicionário

Variáveis do dicionário de dados com potencial preditivo não usadas atualmente:
- `CLASSI_FIN` (classificação etiológica: COVID-19, Influenza, outro) — forte preditor de desfecho
- `TABAG` (tabagismo) — fator de risco relevante
- `RAIOX_RES` (resultado do raio X de tórax: normal/infiltrado/consolidação) — indicador de gravidade
- `PCR_RESUL` / `RES_AN` (resultados laboratoriais) — mas atenção: disponíveis apenas na alta/óbito (risco de leakage)
- `TOMO_RES` (tomografia) — forte indicador clínico de gravidade
- `CRITERIO` (critério de encerramento) — preenchido no fechamento, não usar como feature
