import pandas as pd
import numpy as np

arquivo_origem = "Dados/Raw/archive/pnadc_2024/PNADC_2024_v5.parquet"
arquivo_saida = "Dados/dirty/PNADC_2024_dirty.parquet"

df = pd.read_parquet(arquivo_origem)

# Cópia da base original
df_dirty = df.copy()

# Para tornar o processo reproduzível
np.random.seed(42)

# =========================================
# 1. CRIAR VALORES NULOS EM V1022
# =========================================

indices_nulos = np.random.choice(
    df_dirty.index,
    size=500,
    replace=False
)

df_dirty.loc[indices_nulos, "V1022"] = None

# =========================================
# 2. CRIAR VALORES INVÁLIDOS EM V1022
# Valores válidos: 1 e 2
# Vamos inserir 9
# =========================================

indices_invalidos_v1022 = np.random.choice(
    df_dirty.drop(index=indices_nulos).index,
    size=300,
    replace=False
)

df_dirty.loc[indices_invalidos_v1022, "V1022"] = "9"

# =========================================
# 3. CRIAR VALORES INVÁLIDOS EM V2007
# Valores válidos: 1 e 2
# =========================================

indices_invalidos_v2007 = np.random.choice(
    df_dirty.index,
    size=300,
    replace=False
)

df_dirty.loc[indices_invalidos_v2007, "V2007"] = "9"

# =========================================
# 4. CRIAR VALORES INVÁLIDOS EM V3001
# Valores válidos: 1 e 2
# =========================================

indices_invalidos_v3001 = np.random.choice(
    df_dirty.index,
    size=300,
    replace=False
)

df_dirty.loc[indices_invalidos_v3001, "V3001"] = "9"

# =========================================
# 5. CRIAR VALORES INVÁLIDOS EM V1023
# Valores válidos: 1, 2, 3 e 4
# =========================================

indices_invalidos_v1023 = np.random.choice(
    df_dirty.index,
    size=300,
    replace=False
)

df_dirty.loc[indices_invalidos_v1023, "V1023"] = "9"

# =========================================
# 6. CRIAR DUPLICADOS
# =========================================

duplicados = df_dirty.sample(
    n=500,
    random_state=42
)

df_dirty = pd.concat(
    [df_dirty, duplicados],
    ignore_index=True
)

# =========================================
# SALVAR BASE SUJA
# =========================================

df_dirty.to_parquet(
    arquivo_saida,
    index=False
)

# =========================================
# RELATÓRIO
# =========================================

print("========== BASE DIRTY CRIADA ==========")

print("\nLinhas da base original:")
print(len(df))

print("\nLinhas da base dirty:")
print(len(df_dirty))

print("\nErros inseridos:")

print("Nulos artificiais em V1022:", 500)
print("Valores inválidos em V1022:", 300)
print("Valores inválidos em V2007:", 300)
print("Valores inválidos em V3001:", 300)
print("Valores inválidos em V1023:", 300)
print("Duplicados adicionados:", 500)

print("\nArquivo criado em:")
print(arquivo_saida)
