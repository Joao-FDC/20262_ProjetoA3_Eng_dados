import pandas as pd
import os


# Anos que serão processados
anos = range(2016, 2025)

# Pastas de entrada e saída
pasta_dirty = "Dados/dirty"
pasta_clear = "Dados/clear"

# Cria a pasta clear caso ela não exista
os.makedirs(pasta_clear, exist_ok=True)


# Valores válidos conhecidos para cada variável
VALORES_VALIDOS = {
    "V1022": ["1", "2"],
    "V1023": ["1", "2", "3", "4"],
    "V2007": ["1", "2"],
    "V3001": ["1", "2"]
}


def limpar_coluna(df, coluna, valores_validos):
    """
    Identifica valores inválidos em uma coluna
    e os transforma em valores ausentes (NaN).

    Valores que já eram ausentes permanecem ausentes.
    Nenhum valor é imputado ou criado artificialmente.
    """

    if coluna not in df.columns:
        print(f"Coluna {coluna} não encontrada.")
        return df

    # Identifica valores inválidos.
    # Valores nulos não entram nessa condição.
    mascara_invalida = (
        df[coluna].notna()
        & ~df[coluna].isin(valores_validos)
    )

    quantidade_invalidos = mascara_invalida.sum()

    # Transforma valores inválidos em NaN
    df.loc[mascara_invalida, coluna] = None

    # Conta todos os valores ausentes depois do tratamento
    quantidade_nulos = df[coluna].isna().sum()

    print(
        f"{coluna}: "
        f"{quantidade_invalidos} valores inválidos "
        f"convertidos para NaN | "
        f"{quantidade_nulos} valores ausentes no total"
    )

    return df


for ano in anos:

    print("\n" + "=" * 70)
    print(f"LIMPANDO PNADC {ano}")
    print("=" * 70)

    # Caminho da base DIRTY
    arquivo_dirty = (
        f"{pasta_dirty}/PNADC_{ano}_dirty.parquet"
    )

    # Caminho da base CLEAR
    arquivo_clear = (
        f"{pasta_clear}/PNADC_{ano}_clear.parquet"
    )

    # Verifica se a base DIRTY existe
    if not os.path.exists(arquivo_dirty):

        print("Arquivo DIRTY não encontrado:")
        print(arquivo_dirty)
        continue

    # =========================================================
    # 1. CARREGAR BASE DIRTY
    # =========================================================

    df = pd.read_parquet(arquivo_dirty)

    quantidade_inicial = len(df)

    print(f"Registros DIRTY: {quantidade_inicial}")

    # =========================================================
    # 2. REMOVER REGISTROS DUPLICADOS
    # =========================================================

    quantidade_duplicados = df.duplicated().sum()

    df = df.drop_duplicates()

    print(
        f"Duplicados removidos: "
        f"{quantidade_duplicados}"
    )

    # =========================================================
    # 3. LIMPAR V1022
    # =========================================================

    df = limpar_coluna(
        df,
        "V1022",
        VALORES_VALIDOS["V1022"]
    )

    # =========================================================
    # 4. LIMPAR V1023
    # =========================================================

    df = limpar_coluna(
        df,
        "V1023",
        VALORES_VALIDOS["V1023"]
    )

    # =========================================================
    # 5. LIMPAR V2007
    # =========================================================

    df = limpar_coluna(
        df,
        "V2007",
        VALORES_VALIDOS["V2007"]
    )

    # =========================================================
    # 6. LIMPAR V3001
    # =========================================================

    df = limpar_coluna(
        df,
        "V3001",
        VALORES_VALIDOS["V3001"]
    )

    # =========================================================
    # 7. SALVAR BASE CLEAR
    # =========================================================

    df.to_parquet(
        arquivo_clear,
        index=False
    )

    quantidade_final = len(df)

    print(
        f"Registros CLEAR: "
        f"{quantidade_final}"
    )

    print(
        f"Registros removidos: "
        f"{quantidade_inicial - quantidade_final}"
    )

    print("Arquivo salvo:")
    print(arquivo_clear)


print("\n" + "=" * 70)
print("PROCESSO DE LIMPEZA FINALIZADO")
print("=" * 70)