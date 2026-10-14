import pandas as pd
import os

anos = range(2016, 2025)

pasta_raw = "Dados/Raw/archive"
pasta_dirty = "Dados/dirty"
pasta_clear = "Dados/clear"
pasta_resultado = "Resultado"

os.makedirs(pasta_resultado, exist_ok=True)

# Colunas que foram utilizadas no processo de qualidade
COLUNAS_ANALISE = [
    "V1022",
    "V1023",
    "V2007",
    "V3001"
]

VALORES_VALIDOS = {
    "V1022": ["1", "2"],
    "V1023": ["1", "2", "3", "4"],
    "V2007": ["1", "2"],
    "V3001": ["1", "2"]
}

resultados = []

for ano in anos:

    print("\n" + "=" * 70)
    print(f"ANÁLISE DE QUALIDADE - PNADC {ano}")
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

    if not all(
        os.path.exists(arquivo)
        for arquivo in [arquivo_raw, arquivo_dirty, arquivo_clear]
    ):
        print("Algum arquivo não foi encontrado.")
        continue

    # =========================================================
    # LEITURA
    # =========================================================

    df_raw = pd.read_parquet(arquivo_raw)
    df_dirty = pd.read_parquet(arquivo_dirty)
    df_clear = pd.read_parquet(arquivo_clear)

    # =========================================================
    # DIMENSÕES
    # =========================================================

    raw_linhas = len(df_raw)
    dirty_linhas = len(df_dirty)
    clear_linhas = len(df_clear)

    raw_colunas = len(df_raw.columns)
    dirty_colunas = len(df_dirty.columns)
    clear_colunas = len(df_clear.columns)

    # =========================================================
    # DUPLICADOS
    # =========================================================

    duplicados_raw = df_raw.duplicated().sum()
    duplicados_dirty = df_dirty.duplicated().sum()
    duplicados_clear = df_clear.duplicated().sum()

    # =========================================================
    # VALORES AUSENTES
    # =========================================================

    nulos_raw = df_raw[COLUNAS_ANALISE].isna().sum().sum()
    nulos_dirty = df_dirty[COLUNAS_ANALISE].isna().sum().sum()
    nulos_clear = df_clear[COLUNAS_ANALISE].isna().sum().sum()

    # Percentual de ausências nas colunas analisadas
    total_celulas_raw = raw_linhas * len(COLUNAS_ANALISE)
    total_celulas_dirty = dirty_linhas * len(COLUNAS_ANALISE)
    total_celulas_clear = clear_linhas * len(COLUNAS_ANALISE)

    percentual_nulos_raw = (
        nulos_raw / total_celulas_raw * 100
    )

    percentual_nulos_dirty = (
        nulos_dirty / total_celulas_dirty * 100
    )

    percentual_nulos_clear = (
        nulos_clear / total_celulas_clear * 100
    )

    # =========================================================
    # VALORES INVÁLIDOS
    # =========================================================

    invalidos_raw = 0
    invalidos_dirty = 0
    invalidos_clear = 0

    for coluna in COLUNAS_ANALISE:

        valores_validos = VALORES_VALIDOS[coluna]

        if coluna not in df_raw.columns:
            continue

        mascara_raw = (
            df_raw[coluna].notna()
            & ~df_raw[coluna].isin(valores_validos)
        )

        mascara_dirty = (
            df_dirty[coluna].notna()
            & ~df_dirty[coluna].isin(valores_validos)
        )

        mascara_clear = (
            df_clear[coluna].notna()
            & ~df_clear[coluna].isin(valores_validos)
        )

        invalidos_raw += mascara_raw.sum()
        invalidos_dirty += mascara_dirty.sum()
        invalidos_clear += mascara_clear.sum()

    # =========================================================
    # DIFERENÇAS ENTRE CAMADAS
    # =========================================================

    aumento_dirty = dirty_linhas - raw_linhas
    reducao_clear = dirty_linhas - clear_linhas
    diferenca_final = clear_linhas - raw_linhas

    # =========================================================
    # TAXA DE DUPLICAÇÃO
    # =========================================================

    taxa_duplicados_dirty = (
        duplicados_dirty / dirty_linhas * 100
    )

    taxa_duplicados_clear = (
        duplicados_clear / clear_linhas * 100
    )

    # =========================================================
    # TAXA DE VALORES INVÁLIDOS
    # =========================================================

    taxa_invalidos_dirty = (
        invalidos_dirty /
        (dirty_linhas * len(COLUNAS_ANALISE))
        * 100
    )

    taxa_invalidos_clear = (
        invalidos_clear /
        (clear_linhas * len(COLUNAS_ANALISE))
        * 100
    )

    # =========================================================
    # STATUS
    # =========================================================

    if (
        clear_linhas == raw_linhas
        and duplicados_clear == 0
        and invalidos_clear == 0
    ):
        status = "OK"
    else:
        status = "VERIFICAR"

    # =========================================================
    # EXIBIÇÃO
    # =========================================================

    print(f"Registros RAW:    {raw_linhas}")
    print(f"Registros DIRTY:  {dirty_linhas}")
    print(f"Registros CLEAR:  {clear_linhas}")

    print()
    print(f"Colunas RAW:      {raw_colunas}")
    print(f"Colunas DIRTY:    {dirty_colunas}")
    print(f"Colunas CLEAR:    {clear_colunas}")

    print()
    print(f"Duplicados RAW:   {duplicados_raw}")
    print(f"Duplicados DIRTY: {duplicados_dirty}")
    print(f"Duplicados CLEAR: {duplicados_clear}")

    print()
    print(f"Inválidos RAW:    {invalidos_raw}")
    print(f"Inválidos DIRTY:  {invalidos_dirty}")
    print(f"Inválidos CLEAR:  {invalidos_clear}")

    print()
    print(
        f"Nulos RAW:    {nulos_raw} "
        f"({percentual_nulos_raw:.2f}%)"
    )

    print(
        f"Nulos DIRTY:  {nulos_dirty} "
        f"({percentual_nulos_dirty:.2f}%)"
    )

    print(
        f"Nulos CLEAR:  {nulos_clear} "
        f"({percentual_nulos_clear:.2f}%)"
    )

    print()
    print(f"Aumento RAW → DIRTY: {aumento_dirty}")
    print(f"Redução DIRTY → CLEAR: {reducao_clear}")
    print(f"Diferença RAW → CLEAR: {diferenca_final}")

    print()
    print(
        f"Taxa de duplicados DIRTY: "
        f"{taxa_duplicados_dirty:.4f}%"
    )

    print(
        f"Taxa de inválidos DIRTY: "
        f"{taxa_invalidos_dirty:.4f}%"
    )

    print(
        f"Taxa de inválidos CLEAR: "
        f"{taxa_invalidos_clear:.4f}%"
    )

    print()
    print(f"STATUS: {status}")

    # =========================================================
    # RESULTADO
    # =========================================================

    resultados.append({
        "ano": ano,
        "raw_linhas": raw_linhas,
        "dirty_linhas": dirty_linhas,
        "clear_linhas": clear_linhas,
        "raw_colunas": raw_colunas,
        "dirty_colunas": dirty_colunas,
        "clear_colunas": clear_colunas,
        "duplicados_raw": duplicados_raw,
        "duplicados_dirty": duplicados_dirty,
        "duplicados_clear": duplicados_clear,
        "invalidos_raw": invalidos_raw,
        "invalidos_dirty": invalidos_dirty,
        "invalidos_clear": invalidos_clear,
        "nulos_raw": nulos_raw,
        "nulos_dirty": nulos_dirty,
        "nulos_clear": nulos_clear,
        "percentual_nulos_raw": percentual_nulos_raw,
        "percentual_nulos_dirty": percentual_nulos_dirty,
        "percentual_nulos_clear": percentual_nulos_clear,
        "taxa_duplicados_dirty": taxa_duplicados_dirty,
        "taxa_duplicados_clear": taxa_duplicados_clear,
        "taxa_invalidos_dirty": taxa_invalidos_dirty,
        "taxa_invalidos_clear": taxa_invalidos_clear,
        "aumento_raw_dirty": aumento_dirty,
        "reducao_dirty_clear": reducao_clear,
        "diferenca_raw_clear": diferenca_final,
        "status": status
    })


# =============================================================
# SALVAR RELATÓRIO
# =============================================================

df_resultado = pd.DataFrame(resultados)

arquivo_resultado = (
    f"{pasta_resultado}/"
    "analise_qualidade_2016_2024.csv"
)

df_resultado.to_csv(
    arquivo_resultado,
    index=False
)

print("\n" + "=" * 70)
print("ANÁLISE DE QUALIDADE FINALIZADA")
print("=" * 70)

print(
    df_resultado[
        [
            "ano",
            "raw_linhas",
            "dirty_linhas",
            "clear_linhas",
            "duplicados_dirty",
            "duplicados_clear",
            "invalidos_dirty",
            "invalidos_clear",
            "percentual_nulos_clear",
            "status"
        ]
    ].to_string(index=False)
)

print()
print("Relatório salvo em:")
print(arquivo_resultado)