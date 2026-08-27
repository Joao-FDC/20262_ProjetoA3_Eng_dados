import pandas as pd

arquivo = "Dados/Raw/archive/pnadc_2024/PNADC_2024_v5.parquet"

df = pd.read_parquet(arquivo)

print("========== VALORES ÚNICOS ==========\n")

for coluna in df.columns:
    quantidade = df[coluna].nunique(dropna=True)

    print(f"{coluna}: {quantidade} valores diferentes")

    if quantidade <= 20:
        print(df[coluna].dropna().unique())

    print("-" * 50)