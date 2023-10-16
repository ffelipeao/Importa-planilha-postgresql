import os
import pandas as pd
import psycopg2
import tkinter as tk
from tkinter import filedialog
from decouple import config
import re

def criar_tabela_postgresql_com_nome_arquivo(nome_arquivo_xlsx, db_params):
    try:
        # Leia o arquivo XLSX usando o Pandas
        df = pd.read_excel(nome_arquivo_xlsx)

        # Extraia o nome do arquivo (sem a extensão) para usar como nome da tabela
        nome_arquivo_base = os.path.basename(nome_arquivo_xlsx)
        nome_tabela = nome_arquivo_base.split('.')[0]

        # Substitua caracteres não-alfabéticos nos nomes das colunas
        df.columns = [re.sub(r'[^a-zA-Z0-9]', '', col) for col in df.columns]

        # Crie uma string com a instrução SQL CREATE
        create_sql = f"CREATE TABLE {nome_tabela} ({', '.join([f'{col} text' for col in df.columns])})"

        # Imprima a instrução SQL CREATE na tela
        print("Instrução SQL CREATE:")
        print(create_sql)

        # Conecte-se ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Crie uma tabela no PostgreSQL com os mesmos nomes das colunas no DataFrame
        cur.execute(create_sql)
        conn.commit()

        # Insira os dados do DataFrame na tabela do PostgreSQL
        df.to_sql(nome_tabela, conn, if_exists='replace', index=False)

        # Feche a conexão com o banco de dados
        conn.close()

        return f"Tabela '{nome_tabela}' criada com sucesso no PostgreSQL."
    except Exception as e:
        return f"Erro ao criar a tabela: {str(e)}"


# Leia as informações de conexão do arquivo .env
db_params = {
    'dbname': config('DB_NAME', default='seu_banco_de_dados'),
    'user': config('DB_USER', default='seu_usuario'),
    'password': config('DB_PASSWORD', default='sua_senha'),
    'host': config('DB_HOST', default='localhost'),
    'port': config('DB_PORT', default='5432')
}

# Crie uma janela de diálogo para selecionar o arquivo XLSX
root = tk.Tk()
root.withdraw()  # Ocultar a janela principal
nome_arquivo_xlsx = filedialog.askopenfilename(filetypes=[("Arquivos XLSX", "*.xlsx")])

if nome_arquivo_xlsx:
    # Chame a função para criar a tabela no PostgreSQL
    resultado = criar_tabela_postgresql_com_nome_arquivo(nome_arquivo_xlsx, db_params)

    # Exiba o resultado
    print(resultado)
else:
    print("Nenhum arquivo selecionado.")
