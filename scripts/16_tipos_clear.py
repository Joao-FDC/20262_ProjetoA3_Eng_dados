import pandas as pd

caminho = r"C:\Users\Pichau\OneDrive - Acadêmico - Ânima Educação\Documentos\engenharia_de_dados\projeto_A3\Dados\clear"

df = pd.read_parquet(caminho)

print("=" * 80)
print("MAPEAMENTO DAS VARIÁVEIS PARA SQL")
print("=" * 80)

for coluna in df.columns:

    serie = df[coluna].dropna()

    print("\n" + "-" * 80)
    print(f"COLUNA: {coluna}")
    print(f"Tipo Pandas: {df[coluna].dtype}")
    print(f"Nulos: {df[coluna].isna().sum():,}")
    print(f"Distintos: {df[coluna].nunique(dropna=True):,}")

    if len(serie) > 0:
        print(f"Exemplos: {serie.head(5).tolist()}")