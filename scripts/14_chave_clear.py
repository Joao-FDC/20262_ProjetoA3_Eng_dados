import pandas as pd

caminho = r"C:\Users\Pichau\OneDrive - Acadêmico - Ânima Educação\Documentos\engenharia_de_dados\projeto_A3\Dados\clear"

df = pd.read_parquet(caminho)

print("=" * 70)
print("TESTE DE IDENTIFICAÇÃO DA CLEAR")
print("=" * 70)

print(f"Total de registros: {len(df):,}")

# Combinações candidatas
chaves = [
    ["Ano", "Trimestre", "UPA", "V1008", "V1014"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022"],
    ["Ano", "Trimestre", "UPA", "V1008", "V1014", "V1022", "V1023"],
]

for chave in chaves:

    print("\n" + "-" * 70)
    print("TESTANDO:", chave)

    duplicados = df.duplicated(subset=chave).sum()

    print(f"Duplicados: {duplicados:,}")

    distintos = df.drop_duplicates(subset=chave).shape[0]

    print(f"Registros distintos: {distintos:,}")

    print(f"Registros totais: {len(df):,}")

    if duplicados == 0:
        print(">>> SEM DUPLICATAS NESSA COMBINAÇÃO")
    else:
        print(">>> AINDA EXISTEM DUPLICATAS")