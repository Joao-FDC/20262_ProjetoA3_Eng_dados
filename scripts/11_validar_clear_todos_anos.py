import pandas as pd
import os

anos = range(2016, 2025)

pasta_raw = "Dados/Raw/archive"
pasta_dirty = "Dados/dirty"
pasta_clear = "Dados/clear"
pasta_resultado = "Resultado"

os.makedirs(pasta_resultado, exist_ok=True)

VALORES_VALIDOS = {
    "V1022": ["1", "2"],
    "V1023": ["1", "2", "3", "4"],
    "V2007": ["1", "2"],
    "V3001": ["1", "2"]
}

resultados = []

for ano in anos:

    print("\n" + "=" * 70)
    print(f"VALIDANDO PNADC {ano}")
    print("=" * 70)

    arquivo_raw = (
        f"{pasta_raw}/pnadc_{ano}/"
        f"PNADC_{ano}_v5.parquet"
    )

    arquivo_dirty = (
        f"{pasta_dirty}/"
        f"PNADC_{ano}_dirty.parquet"
    )

    arquivo_clear = (
        f"{pasta_clear}/"
        f"PNADC_{ano}_clear.parquet"
    )

    if not os.path.exists(arquivo_raw):
        print("RAW não encontrado.")
        continue

    if not os.path.exists(arquivo_dirty):
        print("DIRTY não encontrado.")
        continue

    if not os.path.exists(arquivo_clear):
        print("CLEAR não encontrado.")
        continue

    # ---------------------------------------------------------
    # LEITURA DAS BASES
    # ---------------------------------------------------------

    df_raw = pd.read_parquet(arquivo_raw)
    df_dirty = pd.read_parquet(arquivo_dirty)
    df_clear = pd.read_parquet(arquivo_clear)

    # ---------------------------------------------------------
    # QUANTIDADE DE REGISTROS
    # ---------------------------------------------------------

    raw_linhas = len(df_raw)
    dirty_linhas = len(df_dirty)
    clear_linhas = len(df_clear)

    # ---------------------------------------------------------
    # DUPLICADOS
    # ---------------------------------------------------------

    dirty_duplicados = df_dirty.duplicated().sum()
    clear_duplicados = df_clear.duplicated().sum()

    # ---------------------------------------------------------
    # VALORES INVÁLIDOS APÓS A LIMPEZA
    # ---------------------------------------------------------

    invalidos = {}

    for coluna, valores_validos in VALORES_VALIDOS.items():

        if coluna not in df_clear.columns:
            invalidos[coluna] = None
            continue

        mascara_invalida = (
            df_clear[coluna].notna()
            & ~df_clear[coluna].isin(valores_validos)
        )

        invalidos[coluna] = mascara_invalida.sum()

    # ---------------------------------------------------------
    # VALORES AUSENTES
    # ---------------------------------------------------------

    nulos = {}

    for coluna in VALORES_VALIDOS:

        if coluna in df_clear.columns:
            nulos[coluna] = df_clear[coluna].isna().sum()
        else:
            nulos[coluna] = None

    # ---------------------------------------------------------
    # COMPARAÇÃO RAW x DIRTY x CLEAR
    # ---------------------------------------------------------

    diferenca_raw_dirty = dirty_linhas - raw_linhas
    diferenca_dirty_clear = dirty_linhas - clear_linhas
    diferenca_raw_clear = clear_linhas - raw_linhas

    # ---------------------------------------------------------
    # STATUS DA VALIDAÇÃO
    # ---------------------------------------------------------

    erros = []

    # CLEAR deve ter a mesma quantidade de linhas do RAW
    if clear_linhas != raw_linhas:
        erros.append("Quantidade de linhas CLEAR diferente da RAW")

    # DIRTY deve ter 500 registros a mais que RAW
    if diferenca_raw_dirty != 500:
        erros.append("DIRTY não possui exatamente 500 registros adicionais")

    # CLEAR deve remover os 500 duplicados
    if clear_duplicados != 0:
        erros.append("CLEAR ainda possui duplicados")

    # Não pode existir valor inválido nas colunas selecionadas
    for coluna, quantidade in invalidos.items():

        if quantidade is not None and quantidade > 0:
            erros.append(
                f"{coluna} ainda possui {quantidade} valores inválidos"
            )

    status = "OK" if len(erros) == 0 else "ERRO"

    # ---------------------------------------------------------
    # EXIBIÇÃO
    # ---------------------------------------------------------

    print(f"RAW:    {raw_linhas}")
    print(f"DIRTY:  {dirty_linhas}")
    print(f"CLEAR:  {clear_linhas}")

    print()
    print(f"RAW -> DIRTY:   +{diferenca_raw_dirty}")
    print(f"DIRTY -> CLEAR: -{diferenca_dirty_clear}")
    print(f"RAW -> CLEAR:   {diferenca_raw_clear}")

    print()
    print(f"Duplicados DIRTY:  {dirty_duplicados}")
    print(f"Duplicados CLEAR:  {clear_duplicados}")

    print()
    print("Valores inválidos restantes:")

    for coluna, quantidade in invalidos.items():
        print(f"  {coluna}: {quantidade}")

    print()
    print("Valores ausentes na CLEAR:")

    for coluna, quantidade in nulos.items():
        print(f"  {coluna}: {quantidade}")

    print()
    print(f"STATUS: {status}")

    if erros:
        print("Problemas encontrados:")
        for erro in erros:
            print(f"  - {erro}")

    # ---------------------------------------------------------
    # SALVAR RESULTADO
    # ---------------------------------------------------------

    resultados.append({
        "ano": ano,
        "raw_linhas": raw_linhas,
        "dirty_linhas": dirty_linhas,
        "clear_linhas": clear_linhas,
        "raw_dirty_diferenca": diferenca_raw_dirty,
        "dirty_clear_diferenca": diferenca_dirty_clear,
        "raw_clear_diferenca": diferenca_raw_clear,
        "duplicados_dirty": dirty_duplicados,
        "duplicados_clear": clear_duplicados,
        "invalidos_V1022": invalidos["V1022"],
        "invalidos_V1023": invalidos["V1023"],
        "invalidos_V2007": invalidos["V2007"],
        "invalidos_V3001": invalidos["V3001"],
        "nulos_V1022": nulos["V1022"],
        "nulos_V1023": nulos["V1023"],
        "nulos_V2007": nulos["V2007"],
        "nulos_V3001": nulos["V3001"],
        "status": status
    })


# =============================================================
# RELATÓRIO FINAL
# =============================================================

df_resultado = pd.DataFrame(resultados)

arquivo_resultado = (
    f"{pasta_resultado}/"
    "validacao_clear_2016_2024.csv"
)

df_resultado.to_csv(
    arquivo_resultado,
    index=False
)

print("\n" + "=" * 70)
print("VALIDAÇÃO FINALIZADA")
print("=" * 70)

print(df_resultado[
    [
        "ano",
        "raw_linhas",
        "dirty_linhas",
        "clear_linhas",
        "duplicados_clear",
        "invalidos_V1022",
        "invalidos_V1023",
        "invalidos_V2007",
        "invalidos_V3001",
        "status"
    ]
].to_string(index=False))

print()
print(f"Relatório salvo em:")
print(arquivo_resultado)