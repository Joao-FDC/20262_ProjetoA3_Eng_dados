import pandas as pd

caminho = r"C:\Users\Pichau\OneDrive - Acadêmico - Ânima Educação\Documentos\engenharia_de_dados\projeto_A3\Dados\clear"

df = pd.read_parquet(caminho)

print("=" * 70)
print("ESTRUTURA DA CLEAR")
print("=" * 70)

print(f"\nLinhas: {len(df)}")
print(f"Colunas: {len(df.columns)}")

print("\nTIPOS:")
print(df.dtypes)

print("\n" + "=" * 70)
print("EXEMPLO DOS DADOS")
print("=" * 70)

print(df.head(5).to_string())

print("\n" + "=" * 70)
print("VALORES DISTINTOS DE ALGUMAS VARIÁVEIS")
print("=" * 70)

colunas_teste = [
    "Ano",
    "Trimestre",
    "UF",
    "Capital",
    "RM_RIDE",
    "V2007",
    "V2009",
    "V3001",
    "V4009",
    "VD4001",
    "VD4016",
    "VD5001"
]

for coluna in colunas_teste:
    if coluna in df.columns:
        print(f"\n{coluna}:")
        print(df[coluna].value_counts(dropna=False).head(15))