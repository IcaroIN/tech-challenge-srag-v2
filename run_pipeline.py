"""
run_pipeline.py
---------------
Pipeline end-to-end do Tech Challenge SRAG.

Executa sequencialmente:
  1. Carregamento dos dados brutos
  2. Pré-processamento completo
  3. Treinamento dos modelos
  4. Avaliação e geração de visualizações

Uso:
  python run_pipeline.py
  python run_pipeline.py --no-grid-search   # treino rápido sem GridSearchCV
  python run_pipeline.py --no-shap          # pula SHAP (mais rápido)
"""

import argparse
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar os módulos src/
sys.path.insert(0, str(Path(__file__).parent))

from src.load_data import carregar_dataset, inspecionar_dataset, resumo_target
from src.preprocessing import executar_pipeline_preprocessamento
from src.modeling import treinar_todos_modelos
from src.evaluation import avaliar_todos_modelos


def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline ML — SRAG Tech Challenge")
    parser.add_argument(
        "--no-grid-search",
        action="store_true",
        help="Desativa GridSearchCV (treino mais rápido, sem otimização de hiperparâmetros)",
    )
    parser.add_argument(
        "--no-shap",
        action="store_true",
        help="Desativa cálculo de SHAP values (mais rápido)",
    )
    parser.add_argument(
        "--nrows",
        type=int,
        default=None,
        help="Número de linhas a carregar do CSV (útil para testes rápidos, ex: 10000)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("TECH CHALLENGE FASE 1 — CLASSIFICAÇÃO DE SRAG")
    print("=" * 60)

    # 1. Carregamento
    print("\n[ETAPA 1] Carregando dados...")
    df = carregar_dataset(nrows=args.nrows)
    inspecionar_dataset(df)
    resumo_target(df)

    # 2. Pré-processamento
    print("\n[ETAPA 2] Pré-processamento...")
    artefatos = executar_pipeline_preprocessamento(df, salvar=True)
    X_train = artefatos["X_train"]
    X_val   = artefatos["X_val"]
    X_test  = artefatos["X_test"]
    y_train = artefatos["y_train"]
    y_val   = artefatos["y_val"]
    y_test  = artefatos["y_test"]

    # 3. Treinamento
    print("\n[ETAPA 3] Treinamento dos modelos...")
    usar_grid_search = not args.no_grid_search
    modelos = treinar_todos_modelos(X_train, y_train, usar_grid_search=usar_grid_search, salvar=True)

    # Avaliação no conjunto de validação (para acompanhar durante desenvolvimento)
    print("\n[INFO] Avaliação no conjunto de VALIDAÇÃO:")
    from src.evaluation import calcular_metricas
    for nome, modelo in modelos.items():
        calcular_metricas(nome, modelo, X_val, y_val)

    # 4. Avaliação final no conjunto de teste
    print("\n[ETAPA 4] Avaliação final no conjunto de TESTE...")
    calcular_shap = not args.no_shap
    df_resultados = avaliar_todos_modelos(modelos, X_test, y_test, calcular_shap=calcular_shap)

    print("\n" + "=" * 60)
    print("PIPELINE CONCLUÍDO")
    print("=" * 60)
    print(f"\nResultados finais (teste):\n{df_resultados.to_string()}")
    print(f"\nFiguras salvas em: results/figures/")
    print(f"Modelos salvos em: results/models/")
    print(f"Dados processados em: data/processed/")


if __name__ == "__main__":
    main()
