"""
preprocessing.py
----------------
Pipeline de pré-processamento do dataset SIVEP-Gripe.

Etapas:
  1. Filtrar registros com desfecho válido (EVOLUCAO 1=Cura ou 2=Óbito)
  2. Criar variável alvo binária (0=Cura, 1=Óbito)
  3. Selecionar features clínicas relevantes
  4. Tratar valores ausentes
  5. Codificar variáveis categóricas
  6. Normalizar variáveis numéricas
  7. Dividir em treino / validação / teste (70/15/15)
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer


# Diretório de saída para dados processados
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

# Features selecionadas do dataset SIVEP-Gripe
# Divididas em grupos temáticos para facilitar análise
FEATURES_DEMOGRAFICAS = [
    "CS_SEXO",       # Sexo (M/F/I)
    "NU_IDADE_N",    # Idade numérica
    "TP_IDADE",      # Tipo de idade (1=dias, 2=meses, 3=anos)
    "CS_GESTANT",    # Gestante
    "CS_RACA",       # Raça/cor
    "CS_ESCOL_N",    # Escolaridade
    "CS_ZONA",       # Zona de residência (urbana/rural)
]

FEATURES_SINTOMAS = [
    "FEBRE",         # Febre
    "TOSSE",         # Tosse
    "GARGANTA",      # Dor de garganta
    "DISPNEIA",      # Dispneia
    "DESC_RESP",     # Desconforto respiratório
    "SATURACAO",     # Saturação O2 < 95%
    "DIARREIA",      # Diarreia
    "VOMITO",        # Vômito
    "DOR_ABD",       # Dor abdominal
    "FADIGA",        # Fadiga
    "PERD_OLFT",     # Perda de olfato
    "PERD_PALA",     # Perda de paladar
]

FEATURES_COMORBIDADES = [
    "PUERPERA",      # Puérpera
    "CARDIOPATI",    # Doença cardiovascular
    "HEMATOLOGI",    # Doença hematológica
    "SIND_DOWN",     # Síndrome de Down
    "HEPATICA",      # Doença hepática
    "ASMA",          # Asma
    "DIABETES",      # Diabetes
    "NEUROLOGIC",    # Doença neurológica
    "PNEUMOPATI",    # Pneumopatia
    "IMUNODEPRE",    # Imunodepressão
    "RENAL",         # Doença renal
    "OBESIDADE",     # Obesidade
]

FEATURES_INTERNACAO = [
    "HOSPITAL",      # Hospitalizado
    "UTI",           # Internado em UTI
    "SUPORT_VEN",    # Suporte ventilatório
    "NOSOCOMIAL",    # Caso nosocomial
]

FEATURES_VACINA = [
    "VACINA",        # Vacinado contra influenza
    "VACINA_COV",    # Vacinado contra COVID-19
]

# Lista completa de features usadas no modelo
FEATURES = (
    FEATURES_DEMOGRAFICAS
    + FEATURES_SINTOMAS
    + FEATURES_COMORBIDADES
    + FEATURES_INTERNACAO
    + FEATURES_VACINA
)

TARGET = "EVOLUCAO"
TARGET_BINARIO = "OBITO"  # 0=Cura, 1=Óbito


def filtrar_registros_validos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mantém apenas registros com desfecho clínico definitivo: Cura (1) ou Óbito (2).
    Remove registros com EVOLUCAO ausente, ignorada (9) ou óbito por outras causas (3).
    """
    df_filtrado = df[df[TARGET].isin([1, 2])].copy()
    print(f"Registros após filtro de EVOLUCAO válida: {len(df_filtrado):,} ({len(df_filtrado)/len(df)*100:.1f}% do total)")
    return df_filtrado


def criar_target_binario(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria coluna OBITO: 0 = Cura (EVOLUCAO=1), 1 = Óbito (EVOLUCAO=2).
    """
    df = df.copy()
    df[TARGET_BINARIO] = (df[TARGET] == 2).astype(int)
    obitos = df[TARGET_BINARIO].sum()
    total = len(df)
    print(f"Distribuição do target binário — Cura: {total - obitos:,} ({(total-obitos)/total*100:.1f}%) | Óbito: {obitos:,} ({obitos/total*100:.1f}%)")
    return df


def selecionar_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna DataFrame com apenas as features selecionadas e o target binário.
    Colunas ausentes no dataset são ignoradas com aviso.
    """
    colunas_presentes = [c for c in FEATURES if c in df.columns]
    colunas_ausentes = [c for c in FEATURES if c not in df.columns]
    if colunas_ausentes:
        print(f"Aviso: {len(colunas_ausentes)} features não encontradas no dataset: {colunas_ausentes}")
    return df[colunas_presentes + [TARGET_BINARIO]].copy()


def tratar_valores_ausentes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputa valores ausentes:
    - Numéricas: mediana
    - Categóricas (object): moda
    - Binárias/ordinais codificadas (int/float): moda
    """
    df = df.copy()
    colunas_num = df.select_dtypes(include=[np.number]).columns.tolist()
    colunas_num = [c for c in colunas_num if c != TARGET_BINARIO]

    colunas_cat = df.select_dtypes(include=["object"]).columns.tolist()

    if colunas_num:
        imp_num = SimpleImputer(strategy="median")
        df[colunas_num] = imp_num.fit_transform(df[colunas_num])

    if colunas_cat:
        imp_cat = SimpleImputer(strategy="most_frequent")
        df[colunas_cat] = imp_cat.fit_transform(df[colunas_cat])

    pct_nulo = df.isnull().mean().max() * 100
    print(f"Valores ausentes após imputação — máx. por coluna: {pct_nulo:.2f}%")
    return df


def codificar_categoricas(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Codifica variáveis categóricas do tipo object usando LabelEncoder.

    Retorna
    -------
    df_codificado : pd.DataFrame
    encoders : dict  {nome_coluna: LabelEncoder}
    """
    df = df.copy()
    encoders = {}
    for col in df.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    print(f"Colunas codificadas: {list(encoders.keys())}")
    return df, encoders


def normalizar_numericas(
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    Aplica StandardScaler nas features numéricas.
    O scaler é ajustado APENAS no treino e aplicado nos demais splits.

    Retorna
    -------
    X_train, X_val, X_test normalizados e o scaler treinado.
    """
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
    X_val = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns, index=X_val.index)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)
    return X_train, X_val, X_test, scaler


def dividir_dados(
    df: pd.DataFrame,
    test_size: float = 0.15,
    val_size: float = 0.15,
    random_state: int = 42,
) -> tuple:
    """
    Divide o dataset em treino (70%), validação (15%) e teste (15%).
    Usa estratificação para manter proporção do target.

    Retorna
    -------
    X_train, X_val, X_test, y_train, y_val, y_test
    """
    X = df.drop(columns=[TARGET_BINARIO])
    y = df[TARGET_BINARIO]

    # Primeiro split: separa teste
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Segundo split: separa validação do restante
    val_size_ajustado = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size_ajustado, random_state=random_state, stratify=y_temp
    )

    print(f"Split — Treino: {len(X_train):,} | Validação: {len(X_val):,} | Teste: {len(X_test):,}")
    return X_train, X_val, X_test, y_train, y_val, y_test


def executar_pipeline_preprocessamento(df: pd.DataFrame, salvar: bool = True) -> dict:
    """
    Executa o pipeline completo de pré-processamento e opcionalmente salva os artefatos.

    Parâmetros
    ----------
    df : pd.DataFrame — dataset bruto carregado via load_data
    salvar : bool — se True, salva splits e scaler em data/processed/

    Retorna
    -------
    dict com X_train, X_val, X_test, y_train, y_val, y_test, scaler, encoders
    """
    df = filtrar_registros_validos(df)
    df = criar_target_binario(df)
    df = selecionar_features(df)
    df = tratar_valores_ausentes(df)
    df, encoders = codificar_categoricas(df)

    X_train, X_val, X_test, y_train, y_val, y_test = dividir_dados(df)
    X_train, X_val, X_test, scaler = normalizar_numericas(X_train, X_val, X_test)

    artefatos = {
        "X_train": X_train, "X_val": X_val, "X_test": X_test,
        "y_train": y_train, "y_val": y_val, "y_test": y_test,
        "scaler": scaler, "encoders": encoders,
    }

    if salvar:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        X_train.to_parquet(PROCESSED_DIR / "X_train.parquet")
        X_val.to_parquet(PROCESSED_DIR / "X_val.parquet")
        X_test.to_parquet(PROCESSED_DIR / "X_test.parquet")
        y_train.to_frame().to_parquet(PROCESSED_DIR / "y_train.parquet")
        y_val.to_frame().to_parquet(PROCESSED_DIR / "y_val.parquet")
        y_test.to_frame().to_parquet(PROCESSED_DIR / "y_test.parquet")
        joblib.dump(scaler, PROCESSED_DIR / "scaler.pkl")
        joblib.dump(encoders, PROCESSED_DIR / "encoders.pkl")
        print(f"Artefatos salvos em: {PROCESSED_DIR}")

    return artefatos
