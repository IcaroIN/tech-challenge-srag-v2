"""
load_data.py
------------
Funções para carregamento e inspeção inicial do dataset SIVEP-Gripe (INFLUD24).

O dataset é um CSV separado por ponto-e-vírgula (;) com encoding latin-1,
contendo registros de Síndrome Respiratória Aguda Grave (SRAG) hospitalizados.
"""

from pathlib import Path

import pandas as pd


# ============================================================
# Caminhos do projeto
# ============================================================

# __file__ aponta para este arquivo:
# src/tabular/load_data.py
#
# parents[0] = src/tabular
# parents[1] = src
# parents[2] = raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Caminho padrão esperado para o dataset bruto
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "INFLUD24-26-06-2025.csv"


# ============================================================
# Carregamento do dataset
# ============================================================

def carregar_dataset(
    caminho: str | Path = RAW_DATA_PATH,
    nrows: int | None = None
) -> pd.DataFrame:
    """
    Carrega o dataset SIVEP-Gripe a partir de um arquivo CSV.

    Parâmetros
    ----------
    caminho : str ou Path
        Caminho para o arquivo CSV.
        Por padrão usa:
        data/raw/INFLUD24-26-06-2025.csv

    nrows : int, opcional
        Número de linhas a carregar.
        Útil para testes rápidos no notebook.

    Retorna
    -------
    pd.DataFrame
        DataFrame com os dados brutos.
    """

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Dataset não encontrado em:\n{caminho}\n\n"
            "Verifique se o arquivo INFLUD24-26-06-2025.csv está dentro de:\n"
            "data/raw/"
        )

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="latin-1",
        low_memory=False,
        nrows=nrows
    )

    print(
        f"Dataset carregado com sucesso: "
        f"{df.shape[0]:,} registros e {df.shape[1]} colunas"
    )

    return df


# ============================================================
# Inspeção inicial
# ============================================================

def inspecionar_dataset(df: pd.DataFrame) -> None:
    """
    Exibe um resumo inicial do DataFrame.

    Mostra:
    - quantidade de linhas e colunas
    - tipos de dados
    - colunas com mais valores nulos
    - primeiras linhas do dataset

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame a ser inspecionado.
    """

    print("=" * 80)
    print("INSPEÇÃO INICIAL DO DATASET")
    print("=" * 80)

    print(f"\nFormato do dataset: {df.shape[0]:,} linhas e {df.shape[1]} colunas")

    print("\nTipos de dados:")
    print(df.dtypes.value_counts())

    print("\nTop 20 colunas com mais valores nulos:")

    nulos = df.isnull().sum().sort_values(ascending=False)
    pct_nulos = (nulos / len(df) * 100).round(2)

    resumo_nulos = pd.DataFrame({
        "Nulos": nulos,
        "% Nulos": pct_nulos
    })

    print(resumo_nulos.head(20).to_string())

    print("\nPrimeiras 3 linhas do dataset:")
    print(df.head(3).to_string())

    print("=" * 80)


# ============================================================
# Resumo da variável alvo
# ============================================================

def resumo_target(
    df: pd.DataFrame,
    coluna_target: str = "EVOLUCAO"
) -> pd.DataFrame:
    """
    Exibe a distribuição da variável alvo EVOLUCAO.

    Valores esperados no SIVEP-Gripe:
    1 = Cura
    2 = Óbito
    3 = Óbito por outras causas
    9 = Ignorado

    Parâmetros
    ----------
    df : pd.DataFrame
        Dataset carregado.

    coluna_target : str
        Nome da coluna alvo.

    Retorna
    -------
    pd.DataFrame
        Tabela com contagem e percentual por categoria.
    """

    if coluna_target not in df.columns:
        raise ValueError(
            f"A coluna '{coluna_target}' não foi encontrada no dataset."
        )

    mapa_evolucao = {
        1: "Cura",
        2: "Óbito",
        3: "Óbito por outras causas",
        9: "Ignorado"
    }

    contagem = df[coluna_target].value_counts(dropna=False).rename("Contagem")

    percentual = (
        df[coluna_target]
        .value_counts(dropna=False, normalize=True)
        .mul(100)
        .round(2)
        .rename("% Total")
    )

    resumo = pd.concat([contagem, percentual], axis=1)

    resumo.index = resumo.index.map(
        lambda valor: f"{valor} — {mapa_evolucao.get(valor, 'NaN/Outro')}"
    )

    print(f"\nDistribuição da variável alvo '{coluna_target}':")
    print(resumo.to_string())

    return resumo