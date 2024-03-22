import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re
import chardet
import unidecode
import datetime
def format_file_name(file_name):
    # Remover acentos e caracteres especiais
    formatted_name = unidecode.unidecode(file_name)
    # Substituir espaços por underscores (ou outro caractere desejado)
    formatted_name = formatted_name.replace(' ', '_')
    return formatted_name

def detectar_codificacao(arquivo):
    with open(arquivo, 'rb') as f:
        dados = f.read()
        resultado = chardet.detect(dados)
        return resultado['encoding']

# Função para tratar os dados
def tratar_dado(dado):
    if isinstance(dado, str):
        # Se o dado for uma string, remova "_x000D_" e escape aspas simples
        dado_tratado = dado.replace("_x000D_", "").replace("'", "''")
    else:
        # Se o dado não for uma string, converta-o em uma string
        dado_tratado = str(dado)
    return dado_tratado


def gerar_sql(file_list,nome_schema):
    for nome_arquivo in file_list:
        try:
            print('Preparando dados do arquivo:', nome_arquivo)
            # Detectar a codificação do arquivo
            # codificacao = detectar_codificacao(nome_arquivo)
            # Fixar codificacao (utf-8, iso-8859-1 (Latin-1), windows-1252)
            codificacao = 'iso-8859-1'
            print('Carregando dados na memória (df).')
            # Determinar o tipo de arquivo usando a extensão
            extensao = os.path.splitext(nome_arquivo)[1]
            # Ler o arquivo usando Pandas e converter para UTF-8
            if extensao.lower() == '.xlsx':
                df = pd.read_excel(nome_arquivo, engine='openpyxl')
            elif extensao.lower() == '.csv':
                df = pd.read_csv(nome_arquivo, encoding=codificacao, delimiter=';')

            else:
                print("Formato de arquivo não suportado.")
                exit()

            # Remova valores NaN do DataFrame
            # df = df.dropna()
            print('Gerando dados para importa...')
            # Extrair o nome do arquivo (sem a extensão) para usar como nome da tabela
            nome_arquivo_base = os.path.basename(nome_arquivo)
            nome_tabela = nome_arquivo_base.rsplit('.', 1)[0].lower()
            nome_tabela_formatado = format_file_name(nome_tabela)

            # Substitua caracteres não-alfabéticos nos nomes das colunas e converta para minúsculas
            df.columns = [re.sub(r'[^a-zA-Z0-9_]', '', col).lower() for col in df.columns]
            print('Gerando CREATE TABLE...')
            # Crie uma string com a instrução SQL CREATE
            create_sql = f"CREATE TABLE {nome_schema}.\"{nome_tabela_formatado}\" ({', '.join([f'{col} text' for col in df.columns])});"

            print('Gerando INSERT com os dados...')
            # Crie uma string com as instruções SQL INSERT
            insert_sql = f"INSERT INTO {nome_schema}.\"{nome_tabela_formatado}\" ({', '.join(df.columns)}) VALUES\n"
            conta = 0
            for index, row in df.iterrows():
                conta += 1
                if conta % 25000 == 0:
                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print('Data e hora:', current_datetime, '| Linhas processadas:', conta)

                values = ', '.join([f"'{tratar_dado(value)}'" if not pd.isna(value) else 'NULL' for value in row])
                insert_sql += f"({values}),\n"

            # Remova a vírgula extra no final
            insert_sql = insert_sql.rstrip(',\n') + ';'

            # Crie o arquivo SQL com codificação utf-8
            with open(f'sql/{nome_tabela}.sql', 'w', encoding='utf-8') as sql_file:
                sql_file.write(create_sql + '\n')
                sql_file.write(insert_sql)

            print(f'SQL file "{nome_tabela}.sql" successfully created for {nome_arquivo}.')
        except Exception as e:
            print(f'Erro ao criar o arquivo SQL:', e)

if __name__ == "__main__":
    # Registra o horário de início
    hora_inicio = datetime.datetime.now()
    print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
    # Crie uma janela de diálogo para selecionar o arquivo
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    file_list = filedialog.askopenfilenames(filetypes=[("Supported Files", "*.xlsx;*.csv"),])

    if file_list:
        nome_schema = input("Informe o nome do Schema: ")
        print('Gerando dados para o schema:', nome_schema)

        # Chame a função para gerar o arquivo SQL
        gerar_sql(list(file_list),nome_schema)

        # Registra o horário de término
        hora_fim = datetime.datetime.now()
        # Calcula a duração total
        duracao_total = hora_fim - hora_inicio

        print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
        print("Hora final:", hora_fim.strftime("%Y-%m-%d %H:%M:%S"))
        print("Tempo total de execução:", duracao_total)
    else:
        print("Nenhum arquivo selecionado.")
