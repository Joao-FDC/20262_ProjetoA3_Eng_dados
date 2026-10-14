
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "database": "projeto_pnad",
}

TAMANHO_LOTE = 1000

def main():
    conexao = mysql.connector.connect(**DB_CONFIG)
    cursor = conexao.cursor()

    try:
        print("Conectado ao MySQL.")

        # Confere se as tabelas têm as mesmas colunas.
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'projeto_pnad'
              AND TABLE_NAME = 'pnad_clear'
            ORDER BY ORDINAL_POSITION
        """)
        colunas_clear = [linha[0] for linha in cursor.fetchall()]

        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'projeto_pnad'
              AND TABLE_NAME = 'pnad_individual'
            ORDER BY ORDINAL_POSITION
        """)
        colunas_individual = [linha[0] for linha in cursor.fetchall()]

        if colunas_clear != colunas_individual:
            print("ERRO: as estruturas das tabelas são diferentes.")
            print("Colunas pnad_clear:", len(colunas_clear))
            print("Colunas pnad_individual:", len(colunas_individual))
            return

        print(f"Estrutura confirmada: {len(colunas_clear)} colunas.")

        # Compara todas as colunas, por ID, em lotes.
        colunas_dados = [c for c in colunas_clear if c != "id_pnad"]
        lista_colunas = ", ".join(f"`{c}`" for c in colunas_dados)

        cursor.execute("SELECT MAX(id_pnad) FROM pnad_clear")
        max_id = cursor.fetchone()[0] or 0

        total_comparado = 0
        total_diferencas = 0
        inicio = 1

        while inicio <= max_id:
            fim = inicio + TAMANHO_LOTE - 1

            sql = f"""
                SELECT COUNT(*)
                FROM pnad_clear a
                JOIN pnad_individual b ON a.id_pnad = b.id_pnad
                WHERE a.id_pnad BETWEEN %s AND %s
                  AND NOT ({' AND '.join(
                      f'a.`{c}` <=> b.`{c}`' for c in colunas_dados
                  )})
            """

            cursor.execute(sql, (inicio, fim))
            diferencas = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM pnad_clear a
                JOIN pnad_individual b ON a.id_pnad = b.id_pnad
                WHERE a.id_pnad BETWEEN %s AND %s
            """, (inicio, fim))
            comparados = cursor.fetchone()[0]

            total_comparado += comparados
            total_diferencas += diferencas

            print(
                f"IDs {inicio}-{min(fim, max_id)}: "
                f"{comparados} registros comparados; "
                f"{diferencas} registros com diferenças."
            )

            inicio = fim + 1

        print("\n===== RESULTADO FINAL =====")
        print(f"Registros comparados: {total_comparado:,}")
        print(f"Registros com diferenças: {total_diferencas:,}")

        if total_comparado != 3595684:
            print("ATENÇÃO: a quantidade comparada não corresponde ao total esperado.")
        elif total_diferencas == 0:
            print("RESULTADO: conteúdo idêntico nas colunas comparadas.")
        else:
            print("RESULTADO: existem diferenças que precisam ser investigadas.")

    finally:
        cursor.close()
        conexao.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()
