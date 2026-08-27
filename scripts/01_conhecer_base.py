import pandas as pd

arquivo = "Dados/Raw/archive/pnadc_2024/PNADC_2024_v5.parquet"

df = pd.read_parquet(arquivo)

print("Quantidade de linhas:", len(df))
print("Quantidade de colunas:", len(df.columns))

print("\nColunas:")
for coluna in df.columns:
    print(coluna)

print("\nTipos:")
print(df.dtypes)

print("\nPrimeiras linhas:")
print(df.head())