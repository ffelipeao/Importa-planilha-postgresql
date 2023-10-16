import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re


# Função para tratar os dados
def tratar_dado(dado):
    if isinstance(dado, str):
        # Se o dado for uma string, remova "_x000D_" e escape aspas simples
        dado_tratado = dado.replace("_x000D_", "").replace("'", "''")
    else:
        # Se o dado não for uma string, converta-o em uma string
        dado_tratado = str(dado)
    return dado_tratado


def gerar_sql(nome_arquivo_xlsx):
    try:
        # Leia o arquivo XLSX usando o Pandas
        df = pd.read_excel(nome_arquivo_xlsx)

        # Remova valores NaN do DataFrame
        #df = df.dropna()

        # Extraia o nome do arquivo (sem a extensão) para usar como nome da tabela
        nome_arquivo_base = os.path.basename(nome_arquivo_xlsx)
        nome_tabela = nome_arquivo_base.split('.')[0]

        # Substitua caracteres não-alfabéticos nos nomes das colunas
        df.columns = [re.sub(r'[^a-zA-Z0-9]', '', col) for col in df.columns]

        # Crie uma string com a instrução SQL CREATE
        create_sql = f"CREATE TABLE {nome_tabela} ({', '.join([f'{col} text' for col in df.columns])});"

        # Crie uma string com as instruções SQL INSERT
        insert_sql = f"INSERT INTO {nome_tabela} ({', '.join(df.columns)}) VALUES\n"

        for index, row in df.iterrows():
            values = ', '.join([f"'{tratar_dado(value)}'" if not pd.isna(value) else 'NULL' for value in row])
            insert_sql += f"({values}),\n"

        # Remova a vírgula extra no final
        insert_sql = insert_sql.rstrip(',\n') + ';'

        # Crie o arquivo SQL com codificação utf-8
        with open(f'{nome_tabela}.sql', 'w', encoding='utf-8') as sql_file:
            sql_file.write(create_sql + '\n')
            sql_file.write(insert_sql)

        return f'Arquivo SQL "{nome_tabela}.sql" criado com sucesso.'
    except Exception as e:
        return f'Erro ao criar o arquivo SQL: {str(e)}'


# Crie uma janela de diálogo para selecionar o arquivo XLSX
root = tk.Tk()
root.withdraw()  # Ocultar a janela principal
nome_arquivo_xlsx = filedialog.askopenfilename(filetypes=[("Arquivos XLSX", "*.xlsx")])

if nome_arquivo_xlsx:
    # Chame a função para gerar o arquivo SQL
    resultado = gerar_sql(nome_arquivo_xlsx)

    # Exiba o resultado
    print(resultado)
else:
    print("Nenhum arquivo selecionado.")
