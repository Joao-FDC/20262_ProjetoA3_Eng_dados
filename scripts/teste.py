import pandas as pd

caminho = r"C:\Users\Pichau\OneDrive - Acadêmico - Ânima Educação\Documentos\engenharia_de_dados\projeto_A3\Dados\clear"

df = pd.read_parquet(caminho)

chave = [
    "Ano",
    "Trimestre",
    "UPA",
    "V1008",
    "V1014",
    "V1022",
    "V1023",
    "V1030",
    "V1031",
    "V1032",
    "V1034"
]

print("=" * 70)
print("ANÁLISE DAS REPETIÇÕES DA COMBINAÇÃO COMPLETA")
print("=" * 70)

duplicadas = df[df.duplicated(subset=chave, keep=False)].copy()

print(f"\nTotal de registros repetidos: {len(duplicadas):,}")

print(
    f"Combinações repetidas: "
    f"{duplicadas[chave].drop_duplicates().shape[0]:,}"
)

print("\nExemplos das combinações repetidas:")

print(
    duplicadas[chave]
    .value_counts()
    .head(20)
)

print("\nQuantidade de repetições por frequência:")

frequencias = (
    duplicadas[chave]
    .value_counts()
    .value_counts()
    .sort_index()
)

print(frequencias)