import pandas as pd
import numpy as np
import os


# ============================================================
# CONFIGURAÇÕES
# ============================================================

anos = range(2016, 2025)

pasta_raw = "Dados/Raw/archive"
pasta_dirty = "Dados/dirty"

# Cria a pasta dirty caso ela não exista
os.makedirs(pasta_dirty, exist_ok=True)

# Quantidade de erros artificiais
QTD_NULOS = 500
QTD_INVALIDOS = 300
QTD_DUPLICADOS = 500


# ============================================================
# FUNÇÃO PARA ESCOLHER ÍNDICES ALEATÓRIOS
# ============================================================

def escolher_indices(df, quantidade, excluir=None):

    indices = df.index

    if excluir is not None:
        indices = indices.difference(excluir)

    quantidade = min(quantidade, len(indices))

    return np.random.choice(
        indices,
        size=quantidade,
        replace=False
    )


# ============================================================
# PROCESSAR TODOS OS ANOS
# ============================================================

for ano in anos:

    print("\n" + "=" * 60)
    print(f"PROCESSANDO PNADC {ano}")
    print("=" * 60)

    # --------------------------------------------------------
    # Caminhos
    # --------------------------------------------------------

    arquivo_origem = (
        f"{pasta_raw}/pnadc_{ano}/"
        f"PNADC_{ano}_v5.parquet"
    )

    arquivo_saida = (
        f"{pasta_dirty}/"
        f"PNADC_{ano}_dirty.parquet"
    )

    # --------------------------------------------------------
    # Verificar se RAW existe
    # --------------------------------------------------------

    if not os.path.exists(arquivo_origem):

        print("Arquivo RAW não encontrado:")
        print(arquivo_origem)

        continue

    # --------------------------------------------------------
    # Ler base RAW
    # --------------------------------------------------------

    df = pd.read_parquet(arquivo_origem)

    # Criar cópia
    df_dirty = df.copy()

    print("Registros RAW:", len(df))

    # Seed diferente por ano,
    # mas mantendo o processo reproduzível
    np.random.seed(ano)


    # ========================================================
    # 1. V1022
    #
    # Valores válidos:
    # 1 = Urbana
    # 2 = Rural
    #
    # Problemas criados:
    # 500 NULL
    # 300 valores inválidos = 9
    # ========================================================

    indices_nulos_v1022 = []

    if "V1022" in df_dirty.columns:

        # Escolher 500 registros
        indices_nulos_v1022 = escolher_indices(
            df_dirty,
            QTD_NULOS
        )

        # Inserir NULL
        df_dirty.loc[
            indices_nulos_v1022,
            "V1022"
        ] = None

        # Escolher outros 300 registros
        indices_invalidos_v1022 = escolher_indices(
            df_dirty,
            QTD_INVALIDOS,
            excluir=indices_nulos_v1022
        )

        # Inserir código inválido
        df_dirty.loc[
            indices_invalidos_v1022,
            "V1022"
        ] = "9"

        print(
            "V1022:",
            len(indices_nulos_v1022),
            "nulos +",
            len(indices_invalidos_v1022),
            "inválidos"
        )

    else:

        print("V1022 não encontrada.")


    # ========================================================
    # 2. V1023
    #
    # Valores válidos:
    # 1, 2, 3 e 4
    #
    # Problema criado:
    # 300 valores inválidos = 9
    # ========================================================

    if "V1023" in df_dirty.columns:

        indices_invalidos_v1023 = escolher_indices(
            df_dirty,
            QTD_INVALIDOS
        )

        df_dirty.loc[
            indices_invalidos_v1023,
            "V1023"
        ] = "9"

        print(
            "V1023:",
            len(indices_invalidos_v1023),
            "inválidos"
        )

    else:

        print("V1023 não encontrada.")


    # ========================================================
    # 3. V2007
    #
    # Valores válidos:
    # 1 = Homem
    # 2 = Mulher
    #
    # Problema criado:
    # 300 valores inválidos = 9
    # ========================================================

    if "V2007" in df_dirty.columns:

        indices_invalidos_v2007 = escolher_indices(
            df_dirty,
            QTD_INVALIDOS
        )

        df_dirty.loc[
            indices_invalidos_v2007,
            "V2007"
        ] = "9"

        print(
            "V2007:",
            len(indices_invalidos_v2007),
            "inválidos"
        )

    else:

        print("V2007 não encontrada.")


    # ========================================================
    # 4. V3001
    #
    # Valores válidos:
    # 1 = Sim
    # 2 = Não
    #
    # Problema criado:
    # 300 valores inválidos = 9
    # ========================================================

    if "V3001" in df_dirty.columns:

        indices_invalidos_v3001 = escolher_indices(
            df_dirty,
            QTD_INVALIDOS
        )

        df_dirty.loc[
            indices_invalidos_v3001,
            "V3001"
        ] = "9"

        print(
            "V3001:",
            len(indices_invalidos_v3001),
            "inválidos"
        )

    else:

        print("V3001 não encontrada.")


    # ========================================================
    # 5. CRIAR DUPLICADOS
    # ========================================================

    quantidade_duplicados = min(
        QTD_DUPLICADOS,
        len(df_dirty)
    )

    # --------------------------------------------------------
    # IMPORTANTE:
    #
    # Não vamos selecionar registros que receberam NULL
    # artificial em V1022.
    #
    # Isso evita aumentar artificialmente a quantidade
    # de NULLs quando os registros forem duplicados.
    # --------------------------------------------------------

    if "V1022" in df_dirty.columns:

        candidatos_duplicacao = df_dirty[
            df_dirty["V1022"].notna()
        ]

    else:

        candidatos_duplicacao = df_dirty


    duplicados = candidatos_duplicacao.sample(
        n=quantidade_duplicados,
        random_state=ano
    )


    # Adicionar os duplicados na base

    df_dirty = pd.concat(
        [df_dirty, duplicados],
        ignore_index=True
    )


    # ========================================================
    # 6. SALVAR BASE DIRTY
    # ========================================================

    df_dirty.to_parquet(
        arquivo_saida,
        index=False
    )


    # ========================================================
    # 7. RELATÓRIO DO ANO
    # ========================================================

    print(
        "Duplicados adicionados:",
        quantidade_duplicados
    )

    print(
        "Registros DIRTY:",
        len(df_dirty)
    )

    print(
        "Diferença RAW -> DIRTY:",
        len(df_dirty) - len(df)
    )

    print("Arquivo salvo:")
    print(arquivo_saida)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 60)
print("PROCESSAMENTO FINALIZADO")
print("=" * 60)