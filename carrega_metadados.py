import pandas as pd
from conexao import ConexaoBanco
import datetime
import tkinter as tk
from tkinter import filedialog

conn = ConexaoBanco().conectar()
cursor = conn.cursor()

# Criado em 2025-08-15 por Felipe
# Documentação:
#1 - Ler planilha
#2 - Ler colunas da planilha
#3 - Verificar se as colunas existem no banco
#4 - Se existir, verificar se o comentário já existe
#5 - Se existir, verificar se o comentário é o mesmo
#6 - Se não existir, adicionar o comentário


# Lê a planilha
# Registra o horário de início
hora_inicio = datetime.datetime.now()
print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
# Crie uma janela de diálogo para selecionar o arquivo
root = tk.Tk()
root.withdraw()  # Ocultar a janela principal
file_list = filedialog.askopenfilenames(filetypes=[("Supported Files", "*.xlsx;*.csv"),])

if file_list:
    df = pd.read_excel(file_list[0])
    # print(df.columns)
    # print(df.head())

    colunas_nao_encontradas = []

    for _, row in df.iterrows():
        # Remove aspas duplas e simples e espaços em branco
        schema = str(row['schema']).strip('"').strip("'").strip()
        tabela = str(row['tabela']).strip('"').strip("'").strip()
        coluna = str(row['nomecoluna']).strip('"').strip("'").strip().lower()
        comentario = str(row['comentario']).strip('"').strip("'").strip()
        
        # Pula se o comentário estiver vazio ou nulo
        if pd.isna(comentario) or str(comentario).strip() == '' or str(comentario).lower() == 'nan':
            #print(f"Pulando {schema}.{tabela}.{coluna} - comentário vazio")
            continue

        # Verifica se a coluna existe
        cursor.execute("""
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = %s
            AND table_name = %s
            AND lower(column_name) = %s;
        """, (schema, tabela, coluna))

        if cursor.fetchone():
            # Verifica se a coluna já possui comentário
            cursor.execute("""
                SELECT d.description
                FROM pg_catalog.pg_description d
                JOIN pg_catalog.pg_class c ON c.oid = d.objoid
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                JOIN pg_catalog.pg_attribute a ON a.attrelid = c.oid AND a.attnum = d.objsubid
                WHERE n.nspname = %s
                AND c.relname = %s
                AND lower(a.attname) = %s;
            """, (schema, tabela, coluna))
            
            comentario_existente = cursor.fetchone()
            
            if comentario_existente and comentario_existente[0]:
                if comentario_existente[0] != comentario:
                    print(f"Coluna {schema}.{tabela}.{coluna} já possui comentário: '{comentario_existente[0]}'")
                    print(f"Novo comentário seria: '{comentario}'")
                    exit(1)
                else:
                    # print(f"Coluna {schema}.{tabela}.{coluna} já possui comentário. Não há necessidade de atualização.")
                    continue

            # Atualiza o comentário
            cursor.execute(f"""
                COMMENT ON COLUMN "{schema}"."{tabela}"."{coluna}" IS %s;
            """, (comentario,))
            print(f"Comentário atualizado para {schema}.{tabela}.{coluna}")
        else:
            colunas_nao_encontradas.append(f"{schema}.{tabela}.{coluna}")

    conn.commit()
    cursor.close()
    conn.close()

    if colunas_nao_encontradas:
        print("--------------------------------")
        print("--------------------------------")
        print("Colunas não encontradas:")
        for c in colunas_nao_encontradas:
            print(c)
    else:
        print("Todos os comentários atualizados com sucesso!")