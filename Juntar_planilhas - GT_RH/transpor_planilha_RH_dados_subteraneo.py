import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory
from openpyxl import load_workbook

""""
    Felipe Alves - 20241105
    Criado para peparar os dados do GT de Recursos Hídricos.

    O script faz a leitura de cada página(guia) da planilhas, transpoem e junta todas as guias na planilha só de saida.
    As colunas 0, 2, 3 não estão sendo lidas - já que são valores de referência e serão tratados separadamente.

    Entrada: Permite a seleção de varias planilhas no mesmo formato.
    Saída: Para cada planilha lida gera uma nova com páginas unidas transpostas.
"""

# Função para tornar nomes de colunas únicos
def make_unique_columns(columns):
    counts = {}
    unique_columns = []
    for col in columns:
        if col in counts:
            counts[col] += 1
            unique_columns.append(f"{col}_{counts[col]}")
        else:
            counts[col] = 0
            unique_columns.append(col)
    return unique_columns


# Criar uma janela oculta para usar o askopenfilenames
Tk().withdraw()

# Selecionar os arquivos .xlsx (o usuário pode selecionar múltiplos)
arquivos_excel = askopenfilenames(title="Selecione os arquivos .xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])

# Verificar se o usuário selecionou algum arquivo
if not arquivos_excel:
    print("Nenhum arquivo selecionado. O programa será encerrado.")
    exit()

# Selecionar a pasta de saída (onde os arquivos transpostos serão salvos)
# pasta_saida = askdirectory(title="Selecione a pasta de saída")

# Obter o diretório dos arquivos selecionados
diretorio_base = os.path.dirname(arquivos_excel[0])

# Criar a pasta de saída chamada 'Dados_transpostos' no mesmo diretório
pasta_saida = os.path.join(diretorio_base, "Dados_transpostos")
os.makedirs(pasta_saida, exist_ok=True)

# Verificar se o usuário selecionou uma pasta de saída
if not pasta_saida:
    print("Nenhuma pasta de saída selecionada. O programa será encerrado.")
    exit()

# Certificar-se de que a pasta de saída existe
os.makedirs(pasta_saida, exist_ok=True)

# Processar cada arquivo .xlsx selecionado
for caminho_arquivo in arquivos_excel:
    # Extrair o nome do arquivo
    arquivo_excel = os.path.basename(caminho_arquivo)
    print(f"Processando o arquivo: {arquivo_excel}")

    # Carregar todas as abas em um dicionário, pulando as primeiras 10 linhas
    dados_abas = pd.read_excel(caminho_arquivo, sheet_name=None, skiprows=9)

    # Lista para armazenar os DataFrames transpostos
    dados_transpostos_lista = []

    # Abrir o arquivo Excel com openpyxl para verificar colunas e linhas ocultas
    wb = load_workbook(caminho_arquivo, keep_vba=False)

    for nome_aba, df in dados_abas.items():
        # Ignorar abas específicas
        if nome_aba in ['Cronograma', 'Planilha1']:
            continue

        # Acessar a aba com openpyxl
        aba = wb[nome_aba]

        # Remover as colunas 1, 3 e 4 antes de transpor
        colunas_a_remover = [0, 2, 3]
        df = df.drop(df.columns[colunas_a_remover], axis=1, errors='ignore')

        # Transpor o DataFrame
        df_transposto = df.T

        # Definir a primeira linha como cabeçalho e remover a primeira linha (verificação para evitar erros se estiver vazia)
        if not df_transposto.empty and df_transposto.shape[0] > 1:
            df_transposto.columns = df_transposto.iloc[0]  # Define a nova linha de cabeçalho
            df_transposto = df_transposto[1:]  # Remove a linha de cabeçalho antiga
        else:
            print(f"Aba '{nome_aba}' está vazia ou tem formato inesperado e não será processada.")

        # Tornar os nomes das colunas únicos
        df_transposto.columns = make_unique_columns(df_transposto.columns)

        # Remover colunas em branco
        df_transposto = df_transposto.dropna(axis=1, how='all')

        # Adicionar coluna com o nome da aba
        df_transposto['nome_aba'] = nome_aba
        df_transposto['nome_arquivo_origem'] = arquivo_excel

        # Adicionar o DataFrame transposto à lista
        dados_transpostos_lista.append(df_transposto)

    # # Resetando o índice para todos os DataFrames na lista antes de concatenar
    # dados_transpostos_lista = [df.reset_index(drop=True) for df in dados_transpostos_lista]
    #
    # print(df.index.duplicated())  # Verifica quantos índices duplicados existem
    # print(df.index.duplicated().sum())  # Verifica quantos índices duplicados existem
    # # exit()

    # Combinar todos os DataFrames transpostos em um único DataFrame
    df_combined = pd.concat(dados_transpostos_lista, ignore_index=True, sort=False)

    # trabalha o nome do arquivo de saida.
    part_n = arquivo_excel.split('.')
    nome_arquivo_saida = part_n[0] + '_transposto.' + part_n[1]

    # Salvar o DataFrame combinado em um novo arquivo Excel na pasta de saída
    caminho_saida_arquivo = os.path.join(pasta_saida, nome_arquivo_saida)
    df_combined.to_excel(caminho_saida_arquivo, index=False)

    print(f"Arquivo '{caminho_saida_arquivo}' salvo com sucesso!")
