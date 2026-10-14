import pandas as pd

caminho = r"C:\Users\Pichau\OneDrive - Acadêmico - Ânima Educação\Documentos\engenharia_de_dados\projeto_A3\Dados\clear"

df = pd.read_parquet(caminho)

print("=" * 70)
print("ANÁLISE DOS IDENTIFICADORES DA PNAD")
print("=" * 70)

print(f"\nTotal de registros: {len(df):,}")

identificadores = [
    "Ano",
    "Trimestre",
    "UPA",
    "Estrato",
    "V1008",
    "V1014",
    "V1022",
    "V1023",
    "V1030",
    "V1031",
    "V1032",
    "V1034"
]

print("\n" + "=" * 70)
print("VALORES DISTINTOS POR VARIÁVEL")
print("=" * 70)

for coluna in identificadores:
    distintos = df[coluna].nunique(dropna=False)
    print(f"{coluna:12} -> {distintos:,} valores distintos")


print("\n" + "=" * 70)
print("TESTE PROGRESSIVO DE COMBINAÇÕES")
print("=" * 70)

combinacoes = [
    ["Ano", "Trimestre", "UPA"],
    ["Ano", "Trimestre", "UPA", "V1008"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022", "V1023"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022", "V1023", "V1030"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022", "V1023", "V1030", "V1031"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022", "V1023", "V1030", "V1031", "V1032"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022", "V1023", "V1030", "V1031", "V1032", "V1034"]
]

for chave in combinacoes:

    distintos = df[chave].drop_duplicates().shape[0]
    duplicados = len(df) - distintos

    print("\nChave:", " + ".join(chave))
    print(f"Combinações distintas: {distintos:,}")
    print(f"Repetições: {duplicados:,}")