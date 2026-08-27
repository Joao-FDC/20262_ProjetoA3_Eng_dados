import pandas as pd
import os

anos = range(2016, 2025)

pasta_raw = "Dados/Raw/archive"
pasta_dirty = "Dados/dirty"

resultados = []

for ano in anos:

    arquivo_raw = (
        f"{pasta_raw}/pnadc_{ano}/"
        f"PNADC_{ano}_v5.parquet"
    )

    arquivo_dirty = (
        f"{pasta_dirty}/"
        f"PNADC_{ano}_dirty.parquet"
    )

    print("\n" + "=" * 60)
    print(f"VALIDANDO PNADC {ano}")
    print("=" * 60)

    # Verificar se os arquivos existem
    if not os.path.exists(arquivo_raw):
        print("RAW não encontrada.")
        continue

    if not os.path.exists(arquivo_dirty):
        print("DIRTY não encontrada.")
        continue

    df_raw = pd.read_parquet(arquivo_raw)
    df_dirty = pd.read_parquet(arquivo_dirty)

    # =====================================
    # QUANTIDADE DE LINHAS
    # =====================================

    linhas_raw = len(df_raw)
    linhas_dirty = len(df_dirty)
    linhas_adicionadas = linhas_dirty - linhas_raw

    # =====================================
    # DUPLICADOS
    # =====================================

    duplicados = df_dirty.duplicated().sum()

    # =====================================
    # NULOS V1022
    # =====================================

    if "V1022" in df_dirty.columns:

        nulos_raw_v1022 = df_raw["V1022"].isnull().sum()
        nulos_dirty_v1022 = df_dirty["V1022"].isnull().sum()

        diferenca_nulos = (
            nulos_dirty_v1022
            - nulos_raw_v1022
        )

        invalidos_v1022 = (
            df_dirty["V1022"].notna()
            & ~df_dirty["V1022"].isin(["1", "2"])
        ).sum()

    else:

        nulos_raw_v1022 = None
        nulos_dirty_v1022 = None
        diferenca_nulos = None
        invalidos_v1022 = None

    # =====================================
    # V1023
    # =====================================

    if "V1023" in df_dirty.columns:

        invalidos_v1023 = (
            df_dirty["V1023"].notna()
            & ~df_dirty["V1023"].isin(
                ["1", "2", "3", "4"]
            )
        ).sum()

    else:
        invalidos_v1023 = None

    # =====================================
    # V2007
    # =====================================

    if "V2007" in df_dirty.columns:

        invalidos_v2007 = (
            df_dirty["V2007"].notna()
            & ~df_dirty["V2007"].isin(["1", "2"])
        ).sum()

    else:
        invalidos_v2007 = None

    # =====================================
    # V3001
    # =====================================

    if "V3001" in df_dirty.columns:

        invalidos_v3001 = (
            df_dirty["V3001"].notna()
            & ~df_dirty["V3001"].isin(["1", "2"])
        ).sum()

    else:
        invalidos_v3001 = None

    # =====================================
    # STATUS
    # =====================================

    status = "OK"

    if linhas_adicionadas != 500:
        status = "VERIFICAR"

    if duplicados < 500:
        status = "VERIFICAR"

    # =====================================
    # GUARDAR RESULTADO
    # =====================================

    resultados.append({
        "Ano": ano,
        "Linhas_RAW": linhas_raw,
        "Linhas_DIRTY": linhas_dirty,
        "Linhas_adicionadas": linhas_adicionadas,
        "Duplicados": duplicados,
        "Nulos_RAW_V1022": nulos_raw_v1022,
        "Nulos_DIRTY_V1022": nulos_dirty_v1022,
        "Nulos_adicionados_V1022": diferenca_nulos,
        "Invalidos_V1022": invalidos_v1022,
        "Invalidos_V1023": invalidos_v1023,
        "Invalidos_V2007": invalidos_v2007,
        "Invalidos_V3001": invalidos_v3001,
        "Status": status
    })

    print("Linhas RAW:", linhas_raw)
    print("Linhas DIRTY:", linhas_dirty)
    print("Linhas adicionadas:", linhas_adicionadas)
    print("Duplicados encontrados:", duplicados)

    print(
        "Nulos adicionados em V1022:",
        diferenca_nulos
    )

    print(
        "Inválidos V1022:",
        invalidos_v1022
    )

    print(
        "Inválidos V1023:",
        invalidos_v1023
    )

    print(
        "Inválidos V2007:",
        invalidos_v2007
    )

    print(
        "Inválidos V3001:",
        invalidos_v3001
    )

    print("STATUS:", status)


# =========================================
# RELATÓRIO CONSOLIDADO
# =========================================

df_resultados = pd.DataFrame(resultados)

print("\n")
print("=" * 80)
print("RELATÓRIO CONSOLIDADO")
print("=" * 80)

print(df_resultados.to_string(index=False))

# Salvar relatório CSV
arquivo_relatorio = (
    "Resultado/"
    "validacao_dirty_2016_2024.csv"
)

os.makedirs(
    "Resultado",
    exist_ok=True
)

df_resultados.to_csv(
    arquivo_relatorio,
    index=False,
    encoding="utf-8-sig"
)

print("\nRelatório salvo em:")
print(arquivo_relatorio)