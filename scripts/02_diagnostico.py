import pandas as pd

arquivo = "Dados/Raw/archive/pnadc_2024/PNADC_2024_v5.parquet"

df = pd.read_parquet(arquivo)

print("========== DIAGNÓSTICO DA BASE ==========")

print("\nQuantidade de linhas:")
print(len(df))

print("\nQuantidade de colunas:")
print(len(df.columns))

print("\n========== VALORES NULOS ==========")

nulos = df.isnull().sum()

print(nulos[nulos > 0])

print("\n========== DUPLICADOS ==========")

print("Quantidade de registros duplicados:", df.duplicated().sum())

print("\n========== TIPOS DE DADOS ==========")

print(df.dtypes)

print("\n========== PRIMEIRAS 5 LINHAS ==========")

print(df.head())