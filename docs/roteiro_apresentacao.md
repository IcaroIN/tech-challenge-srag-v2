# Roteiro de Apresentação — Tech Challenge Fase 1
## Classificação de Desfecho Clínico em SRAG (SIVEP-Gripe)
### FIAP Pos-Tech — Machine Learning Engineering
### Formato: vídeo de até 15 minutos

---

> **Como usar este roteiro:** cada bloco tem um tempo-alvo e um script de fala sugerido. O script não precisa ser lido palavra a palavra — use como guia do que dizer enquanto mostra o notebook ou os gráficos.

---

## Bloco 1 — Contexto e Problema
**Tempo-alvo: 1m30s | Acumulado: 0:00 → 1:30**

### O que mostrar
Slide ou célula de abertura do notebook 01.

### Script de fala

"O projeto resolve um problema real de saúde pública: com base nos dados clínicos disponíveis na internação, é possível prever se um paciente com SRAG — Síndrome Respiratória Aguda Grave — vai se curar ou morrer?

Os dados vêm do SIVEP-Gripe, o sistema do Ministério da Saúde que registra todos os casos hospitalizados de SRAG no Brasil. O dataset tem aproximadamente 268 mil registros e 194 variáveis — um problema de classificação binária supervisionada em escala real.

Por que isso importa? Porque UTI, ventilação mecânica e medicamentos são recursos escassos. Um modelo que identifica pacientes de alto risco na admissão pode ajudar equipes clínicas a priorizar quem precisa de atenção imediata."

---

## Bloco 2 — Dataset, Formulação e Desbalanceamento
**Tempo-alvo: 1m30s | Acumulado: 1:30 → 3:00**

### O que mostrar
Célula do notebook 01 com `resumo_target()` — distribuição da variável `EVOLUCAO`.

### Script de fala

"A variável alvo é `EVOLUCAO`. Filtramos apenas os valores 1 — Cura — e 2 — Óbito. Registros com desfecho ignorado ou óbito por outras causas são removidos porque não representam um desfecho clínico definitivo e interpretável.

O dataset é desbalanceado: a maioria dos pacientes sobrevive. Para compensar, todos os modelos sklearn usam `class_weight='balanced'`, e o XGBoost usa `scale_pos_weight` calculado automaticamente como a razão entre o número de curas e óbitos no treino. Sem esse ajuste, os modelos ignorariam a classe minoritária — exatamente a mais crítica clinicamente."

---

## Bloco 3 — Seleção de Features
**Tempo-alvo: 1m00s | Acumulado: 3:00 → 4:00**

### O que mostrar
Tabela ou constante `FEATURES_*` do `src/tabular/preprocessing.py`, ou slide com os 5 grupos.

### Script de fala

"Selecionamos 35 features clínicas organizadas em 5 grupos: demográficas, sintomas na admissão, comorbidades, dados de internação e vacinação.

O critério principal foi disponibilidade na admissão — só usamos variáveis coletadas na entrada do paciente. Variáveis preenchidas depois do desfecho, como data de óbito, número da declaração de óbito e critério de encerramento, foram deliberadamente excluídas para evitar data leakage."

---

## Bloco 4 — Pipeline de Dados e Anti-Leakage
**Tempo-alvo: 1m30s | Acumulado: 4:00 → 5:30**

### O que mostrar
Fluxo do pipeline no notebook 02 ou diagrama do preprocessamento.

### Script de fala

"O pipeline segue essa ordem: filtrar desfechos válidos, criar o target binário, selecionar as 35 features — e só então fazer o split estratificado 70/15/15.

Essa ordem é crítica. O split acontece antes de qualquer transformação. Imputadores, encoders e o StandardScaler são fitados exclusivamente no conjunto de treino e aplicados via `transform` nos demais. Isso garante que as métricas finais reflitam desempenho real em dados nunca vistos.

O conjunto de validação é usado só para o GridSearchCV. O conjunto de teste é tocado uma única vez, na avaliação final."

---

## Bloco 5 — Modelos e Tuning
**Tempo-alvo: 1m00s | Acumulado: 5:30 → 6:30**

### O que mostrar
Tabela comparativa dos 4 modelos no notebook 03.

### Script de fala

"Treinamos 4 modelos: Regressão Logística como baseline linear interpretável, Árvore de Decisão para regras explícitas, Random Forest como ensemble robusto, e XGBoost como o modelo de maior performance esperada.

Todos passam por GridSearchCV com StratifiedKFold de 5 folds, otimizando F1-score da classe positiva. Os melhores hiperparâmetros são selecionados automaticamente e o modelo final é retreinado no conjunto de treino completo."

---

## Bloco 6 — Avaliação: Métricas, Escolha e Visualizações
**Tempo-alvo: 2m00s | Acumulado: 6:30 → 8:30**

### O que mostrar
- Tabela comparativa de métricas (notebook 04)
- Um `confusion_matrix_*.png`
- `roc_curves.png`
- Um `shap_summary_*.png`

### Script de fala

"A métrica principal é o F1-score da classe Óbito. Em dados desbalanceados, accuracy é enganosa: um modelo que prevê sempre 'Cura' já teria alta accuracy sem nenhum valor clínico. F1 equilibra precision e recall para a classe que realmente importa.

ROC-AUC é usada como complemento por ser robusta ao desbalanceamento e permitir comparar os modelos independentemente do threshold de decisão.

[mostrar confusion matrix] A matriz de confusão mostra os falsos negativos — pacientes que morreram e o modelo classificou como Cura. Esses são os erros mais caros clinicamente.

[mostrar SHAP] O SHAP vai além da importância de features: ele mostra em que direção cada variável empurra a predição. Saturação baixa, suporte ventilatório invasivo e idade elevada aumentam a probabilidade de Óbito — o que é consistente com a literatura clínica e indica que o modelo aprendeu padrões plausíveis, não artefatos dos dados."

---

## Bloco 7 — Discussão Crítica e Aplicabilidade Clínica
**Tempo-alvo: 2m30s | Acumulado: 8:30 → 11:00**

### O que mostrar
Slide de discussão ou retornar ao SHAP e à tabela de métricas para ilustrar os pontos.

### Script de fala

"Agora a pergunta mais importante: esse modelo pode ser usado na prática?

Como ferramenta de apoio à decisão, sim. Como substituto do julgamento clínico, não.

O modelo produz um score de risco — a probabilidade estimada de óbito dado o perfil clínico na admissão. Esse score pode ser útil em triagem de pronto-socorro, na priorização de leitos de UTI quando a demanda excede a oferta, e em vigilância epidemiológica para identificar perfis populacionais de risco.

O fluxo correto de uso é: o modelo sinaliza risco, o médico avalia o contexto completo, e o médico decide. O médico sempre tem a palavra final. Existem razões estruturais para isso: o modelo foi treinado em dados históricos e pode não generalizar para novos agentes virais ou contextos epidemiológicos diferentes. Ele não tem acesso ao exame físico, à evolução nas primeiras horas nem ao histórico completo que o médico avalia presencialmente. E features faltantes degradam a predição silenciosamente.

Uma reflexão importante sobre threshold: o modelo por padrão usa 0.5 como ponto de corte. Mas clinicamente, errar um óbito como Cura é muito mais custoso do que o inverso. Em produção, o threshold deveria ser ajustado abaixo de 0.5 para maximizar recall da classe Óbito — com aceitação de mais falsos positivos, que nesse contexto é preferível.

Por fim, há uma limitação que precisa ser reconhecida: variáveis como UTI e suporte ventilatório podem ser atualizadas durante a internação, não só na admissão. Se forem preenchidas após piora clínica, introduzem leakage parcial. É o principal ponto de auditoria para uma versão de produção."

---

## Bloco 8 — Validação Complementar com Imagens
**Tempo-alvo: 1m30s | Acumulado: 11:00 → 12:30**

### O que mostrar
Notebook 05 — exemplos de radiografias e a matriz de confusão da CNN.

### Script de fala

"Como validação complementar, implementamos um segundo pipeline usando deep learning para classificação de radiografias de tórax. O dataset é o COVID-19 Radiography Database do Kaggle, com 4 classes: Normal, COVID, Opacidade Pulmonar e Pneumonia Viral.

Treinamos uma CNN própria do zero — sem transfer learning — usando Keras. A escolha foi intencional: o objetivo era praticar o pipeline completo de deep learning, não adaptar um modelo pronto. A arquitetura usa GlobalAveragePooling2D em vez de Flatten, o que reduziu o modelo de 23 milhões para menos de 24 mil parâmetros — adequado ao tamanho do dataset de 1.200 imagens.

A avaliação gera relatório de classificação com precision, recall e F1 por classe, e matriz de confusão visualizada."

---

## Bloco 9 — Próximos Passos e Encerramento
**Tempo-alvo: 1m00s | Acumulado: 12:30 → 13:30**

### O que mostrar
Slide final ou retorno à estrutura do projeto.

### Script de fala

"Os principais próximos passos para o pipeline tabular são: substituir o código 9=Ignorado por NaN antes da imputação, ajustar o threshold de decisão para maximizar recall de Óbito, calibrar as probabilidades do XGBoost com CalibratedClassifierCV, e adicionar features ainda não incluídas como tabagismo e resultado do raio-X, após confirmar que estão disponíveis na admissão.

Para o pipeline de imagem: aumentar o dataset, adicionar Dropout para regularização, e implementar early stopping.

O código está organizado em módulos reutilizáveis em `src/tabular/` e `src/image/`, com 18 testes automatizados cobrindo as invariantes críticas do pipeline — filtro de target, ausência de leakage, stratificação correta, e reprodutibilidade com seed 42 em todos os pontos de aleatoriedade."

---

## Resumo de Tempo

| Bloco | Tema | Tempo | Acumulado |
|-------|------|-------|-----------|
| 1 | Contexto e problema | 1m30s | 1:30 |
| 2 | Dataset, formulação e desbalanceamento | 1m30s | 3:00 |
| 3 | Seleção de features | 1m00s | 4:00 |
| 4 | Pipeline de dados e anti-leakage | 1m30s | 5:30 |
| 5 | Modelos e tuning | 1m00s | 6:30 |
| 6 | Avaliação: métricas, escolha e visualizações | 2m00s | 8:30 |
| 7 | Discussão crítica e aplicabilidade clínica | 2m30s | 11:00 |
| 8 | Validação complementar com imagens | 1m30s | 12:30 |
| 9 | Próximos passos e encerramento | 1m00s | 13:30 |
| — | Margem para transições e respiração | 1m30s | **15:00** |

---

## Checklist da Rubrica

- [x] Avaliação com dados de teste (accuracy, recall, F1-score) → Bloco 6
- [x] Discussão sobre escolha da métrica → Bloco 6 (F1 vs accuracy em dados desbalanceados)
- [x] Feature importance → Bloco 6
- [x] SHAP → Bloco 6
- [x] Discussão crítica dos resultados → Bloco 7
- [x] Aplicabilidade prática do modelo → Bloco 7
- [x] Papel do médico como decisor final → Bloco 7
