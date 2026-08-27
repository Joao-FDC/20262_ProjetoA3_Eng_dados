import pandas as pd

arquivo = "Dados/dirty/PNADC_2024_dirty.parquet"

df = pd.read_parquet(arquivo)

total_registros = len(df)

# =========================================
# REGRAS
# =========================================

validos_v1022 = ["1", "2"]
validos_v1023 = ["1", "2", "3", "4"]
validos_v2007 = ["1", "2"]
validos_v3001 = ["1", "2"]
validos_vd4001 = ["1", "2"]

# =========================================
# DUPLICADOS
# =========================================

duplicados = df.duplicated().sum()

unicidade = (
    (total_registros - duplicados)
    / total_registros
) * 100

# =========================================
# COMPLETUDE
# =========================================

colunas_completude = [
    "V1022",
    "V1023",
    "V2007",
    "V3001",
    "VD4001"
]

total_campos = (
    total_registros
    * len(colunas_completude)
)

total_nulos = (
    df[colunas_completude]
    .isnull()
    .sum()
    .sum()
)

completude = (
    (total_campos - total_nulos)
    / total_campos
) * 100

# =========================================
# VALIDADE
# =========================================

def contar_invalidos(coluna, valores_validos):
    return (
        df[coluna].notna()
        & ~df[coluna].isin(valores_validos)
    ).sum()


invalidos_v1022 = contar_invalidos(
    "V1022",
    validos_v1022
)

invalidos_v1023 = contar_invalidos(
    "V1023",
    validos_v1023
)

invalidos_v2007 = contar_invalidos(
    "V2007",
    validos_v2007
)

invalidos_v3001 = contar_invalidos(
    "V3001",
    validos_v3001
)

invalidos_vd4001 = contar_invalidos(
    "VD4001",
    validos_vd4001
)

total_invalidos = (
    invalidos_v1022
    + invalidos_v1023
    + invalidos_v2007
    + invalidos_v3001
    + invalidos_vd4001
)

campos_nao_nulos = (
    total_campos
    - total_nulos
)

validade = (
    (campos_nao_nulos - total_invalidos)
    / campos_nao_nulos
) * 100

# =========================================
# QUALIDADE GERAL
# =========================================

qualidade_geral = (
    completude
    + validade
    + unicidade
) / 3

# =========================================
# RESULTADO
# =========================================

print("========== RELATÓRIO DE QUALIDADE ==========")

print("\nTotal de registros:")
print(total_registros)

print("\nDuplicados:")
print(duplicados)

print("\nNulos analisados:")
print(total_nulos)

print("\nValores inválidos:")
print(total_invalidos)

print("\n========== INDICADORES ==========")

print(f"Completude: {completude:.2f}%")
print(f"Validade: {validade:.2f}%")
print(f"Unicidade: {unicidade:.2f}%")

print(
    f"Qualidade geral: "
    f"{qualidade_geral:.2f}%"
)