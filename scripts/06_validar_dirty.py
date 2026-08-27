import pandas as pd

arquivo = "Dados/dirty/PNADC_2024_dirty.parquet"

df = pd.read_parquet(arquivo)

print("========== VALIDAÇÃO DA BASE DIRTY ==========\n")

# =========================================
# 1. DUPLICADOS
# =========================================

duplicados = df.duplicated().sum()

print("Duplicados encontrados:")
print(duplicados)

print("-" * 50)

# =========================================
# 2. NULOS EM V1022
# =========================================

nulos_v1022 = df["V1022"].isnull().sum()

print("Nulos em V1022:")
print(nulos_v1022)

print("-" * 50)

# =========================================
# 3. VALORES INVÁLIDOS EM V1022
# Valores válidos: 1 e 2
# =========================================

validos_v1022 = ["1", "2"]

invalidos_v1022 = df[
    df["V1022"].notna() &
    ~df["V1022"].isin(validos_v1022)
]

print("Valores inválidos em V1022:")
print(len(invalidos_v1022))

print("Valores encontrados:")
print(invalidos_v1022["V1022"].value_counts())

print("-" * 50)

# =========================================
# 4. VALORES INVÁLIDOS EM V1023
# Valores válidos: 1, 2, 3 e 4
# =========================================

validos_v1023 = ["1", "2", "3", "4"]

invalidos_v1023 = df[
    df["V1023"].notna() &
    ~df["V1023"].isin(validos_v1023)
]

print("Valores inválidos em V1023:")
print(len(invalidos_v1023))

print("Valores encontrados:")
print(invalidos_v1023["V1023"].value_counts())

print("-" * 50)

# =========================================
# 5. VALORES INVÁLIDOS EM V2007
# Valores válidos: 1 e 2
# =========================================

validos_v2007 = ["1", "2"]

invalidos_v2007 = df[
    df["V2007"].notna() &
    ~df["V2007"].isin(validos_v2007)
]

print("Valores inválidos em V2007:")
print(len(invalidos_v2007))

print("Valores encontrados:")
print(invalidos_v2007["V2007"].value_counts())

print("-" * 50)

# =========================================
# 6. VALORES INVÁLIDOS EM V3001
# Valores válidos: 1 e 2
# =========================================

validos_v3001 = ["1", "2"]

invalidos_v3001 = df[
    df["V3001"].notna() &
    ~df["V3001"].isin(validos_v3001)
]

print("Valores inválidos em V3001:")
print(len(invalidos_v3001))

print("Valores encontrados:")
print(invalidos_v3001["V3001"].value_counts())

print("-" * 50)

# =========================================
# 7. RESUMO
# =========================================

print("\n========== RESUMO ==========")

print("Duplicados:", duplicados)
print("Nulos V1022:", nulos_v1022)
print("Inválidos V1022:", len(invalidos_v1022))
print("Inválidos V1023:", len(invalidos_v1023))
print("Inválidos V2007:", len(invalidos_v2007))
print("Inválidos V3001:", len(invalidos_v3001))
