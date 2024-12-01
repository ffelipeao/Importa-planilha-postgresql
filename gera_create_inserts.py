import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re
import chardet
import unidecode
import datetime
from executa_arquivo_sql import execute_sql_file

def format_file_name(file_name):
    # Remover acentos e caracteres especiais
    formatted_name = unidecode.unidecode(file_name).strip()
    # Substituir espaços por underscores
    formatted_name = formatted_name.replace(' ', '_')
    # Substituir múltiplos underscores por um único
    formatted_name = re.sub(r'_{2,}', '_', formatted_name)
    return formatted_name

def detectar_codificacao(arquivo):
    with open(arquivo, 'rb') as f:
        dados = f.read()
        resultado = chardet.detect(dados)
        return resultado['encoding']


#removido em 20241130
# Função para tratar os dados
# def tratar_dado(dado):
#     if isinstance(dado, str):
#         # Se o dado for uma string, remova "_x000D_" e escape aspas simples
#         dado_tratado = dado.replace("_x000D_", "").replace("'", "''")
#     else:
#         # Se o dado não for uma string, converta-o em uma string
#         dado_tratado = str(dado)
#     return dado_tratado

# Função para tratar os dados
def tratar_dado(dado):
    if isinstance(dado, str):
        # Se o dado for uma string, remova "_x000D_" e escape aspas simples
        dado_tratado = dado.replace("_x000D_", "").replace("'", "''")
    elif isinstance(dado, float):
        # Se o dado for float, e tiver um valor inteiro, converta para inteiro (sem .0)
        if dado.is_integer():
            dado_tratado = str(int(dado))  # Remove o ".0"
        else:
            dado_tratado = str(dado)  # Mantém o número flutuante com casas decimais
    else:
        # Se o dado não for uma string ou float, converta-o em uma string
        dado_tratado = str(dado)
    return dado_tratado



def gerar_sql(file_list,nome_schema):

    for nome_arquivo in file_list:
        try:
            print('Preparando dados do arquivo:', nome_arquivo)
            # Detectar a codificação do arquivo
            # codificacao = detectar_codificacao(nome_arquivo)
            # Fixar codificacao (utf-8, iso-8859-1 (Latin-1), windows-1252)
            # codificacao = 'iso-8859-1'
            # codific = input("Informe a codificacao (Ex.: 1- utf-8;  2- iso-8859-1 (Latin-1); 3- windows-1252): ")
            codific = '1'
            if codific == '1':
                codificacao = 'utf-8'
            elif codific == '2':
                codificacao = 'iso-8859-1'
            elif codific == '3':
                codificacao = 'windows-1252'
            else:
                codificacao = codific
            print('Codificação selecionada:', codificacao)

            print('Carregando dados na memória (df).')
            # Determinar o tipo de arquivo usando a extensão
            extensao = os.path.splitext(nome_arquivo)[1]
            # Ler o arquivo usando Pandas e converter para UTF-8
            if extensao.lower() == '.xlsx':
                df = pd.read_excel(nome_arquivo, engine='openpyxl')
            elif extensao.lower() == '.csv':
                df = pd.read_csv(nome_arquivo, encoding=codificacao, delimiter=';', low_memory=False)
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
            df.columns = [re.sub(r'[^a-zA-Z0-9_]', '', format_file_name(col)).lower() for col in df.columns]
            print('Gerando CREATE TABLE...')
            # Crie uma string com a instrução SQL CREATE
            #create_sql = f"CREATE TABLE {nome_schema}.\"{nome_tabela_formatado}\" ({', '.join([f'{col} text' for col in df.columns])});"
            # Crie uma string com a instrução SQL CREATE
            create_sql = f"CREATE TABLE {nome_schema}.\"{nome_tabela_formatado}\" (" \
                         + ', '.join([f'\"{col}\" text' for col in df.columns]) + ");"

            print('Gerando INSERT com os dados...')
            # Crie uma string com as instruções SQL INSERT
            #insert_sql = f"INSERT INTO {nome_schema}.\"{nome_tabela_formatado}\" ({', '.join(df.columns)}) VALUES\n"
            # Crie uma string com as instruções SQL INSERT
            insert_sql = f"INSERT INTO {nome_schema}.\"{nome_tabela_formatado}\" (" \
                         + ', '.join([f'\"{col}\"' for col in df.columns]) + ") VALUES\n"

            total_linhas = df.shape[0]
            print("Total de linhas no DataFrame:", total_linhas)

            conta = 0
            for index, row in df.iterrows():
                conta += 1
                if conta % 25000 == 0:
                    # Supondo que 'conta' seja o número de linhas processadas e 'total_linhas' seja o número total de linhas no DataFrame
                    porcentagem = round((conta / total_linhas) * 100, 2)
                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print('Data e hora:', current_datetime, '| Linhas processadas:', conta, ' - ', porcentagem, "%")

                values = ', '.join([f"'{tratar_dado(value)}'" if not pd.isna(value) else 'NULL' for value in row])
                insert_sql += f"({values}),\n"

            # Remova a vírgula extra no final
            insert_sql = insert_sql.rstrip(',\n') + ';'

            print("Escrevendo arquivo .sql")
            # Crie o arquivo SQL com codificação utf-8
            with open(f'sql/{nome_tabela}.sql', 'w', encoding='utf-8') as sql_file:
                sql_file.write(create_sql + '\n')
                sql_file.write(insert_sql)

            print(f'O arquvo SQL "{nome_tabela}.sql" foi criado com sucesso para {nome_arquivo}.')

            print('###' * 50)
            print('###' * 15, "Inserindo no Banco de dados", '###' * 15)
            print('    Executando script sql: ', nome_tabela+'.sql')
            if execute_sql_file('sql/' + nome_tabela+'.sql'):
                print(f'    Inserido com Sucesso!')
            else:
                print(f'    Erro ao inserir os dados do arquivo sql/{nome_tabela}.sql ')
            print('###' * 50)

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
        # nome_schema = input("Informe o nome do Schema: ")
        nome_schema = 'dados_gts'
        print('Gerando dados para o schema:', nome_schema)

        # Chame a função para gerar o arquivo SQL
        gerar_sql(list(file_list),nome_schema)

        print('Gerado com sucesso!!!')
        # Registra o horário de término
        hora_fim = datetime.datetime.now()
        # Calcula a duração total
        duracao_total = hora_fim - hora_inicio

        print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
        print("Hora final:", hora_fim.strftime("%Y-%m-%d %H:%M:%S"))
        print("Tempo total de execução:", duracao_total)
    else:
        print("Nenhum arquivo selecionado.")
