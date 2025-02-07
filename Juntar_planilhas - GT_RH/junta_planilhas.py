import pandas as pd
import os
import re
import unidecode
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory

""""
    Felipe Alves - 20241105
    Criado para preparar os dado do GT de Recursos Hídricos.
    
    O script junta as planilhas com apenas uma página e que já estão transpostas na forma vertical 
    Pode ser configurada para pular as linhas com valores de referencia
        Para pular a leitura das linhas 2 e 3 com o atributo (skiprows=[1, 2] - linha 66) - valores de referencia - tratados separadamente.
    
    Entrada: Permite a seleção de varias planilhas no mesmo formato.
    Saída: Uma unica planilha com os dados unidos.
"""

def format_file_name(file_name):
    # Remover acentos e caracteres especiais
    formatted_name = unidecode.unidecode(file_name).strip()
    # Substituir espaços por underscores
    formatted_name = formatted_name.replace(' ', '_')
    # Substituir múltiplos underscores por um único
    formatted_name = re.sub(r'_{2,}', '_', formatted_name)
    return formatted_name

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

# Selecionar a pasta de saída (onde os arquivos combinados serão salvos)
pasta_saida = askdirectory(title="Selecione a pasta de saída")

# Verificar se o usuário selecionou uma pasta de saída
if not pasta_saida:
    print("Nenhuma pasta de saída selecionada. O programa será encerrado.")
    exit()

# Certificar-se de que a pasta de saída existe
os.makedirs(pasta_saida, exist_ok=True)

# DataFrame vazio para armazenar os dados combinados
df_combined = pd.DataFrame()

# Processar cada arquivo .xlsx selecionado
for caminho_arquivo in arquivos_excel:
    # Extrair o nome do arquivo
    arquivo_excel = os.path.basename(caminho_arquivo)
    print(f"Processando o arquivo: {arquivo_excel}")

    # sheets = pd.ExcelFile(caminho_arquivo).sheet_names
    # print("Abas disponíveis:", sheets)
    # exit()
    # Carregar a primeira aba do arquivo Excel, pulando as linhas 2 e 3 (índices 1 e 2)
    # Remover "skiprows=[1, 2]" caso queira manter todas as linhas
    dados_aba = pd.read_excel(caminho_arquivo, sheet_name=0)
    # print(dados_aba.head())  # Verifica se os dados foram carregados corretamente
    # exit()
    # Substitua caracteres não-alfabéticos nos nomes das colunas e converta para minúsculas
    dados_aba.columns  = [re.sub(r'[^a-zA-Z0-9_]', '', format_file_name(col)).lower() for col in dados_aba.columns ]

    # Tornar os nomes das colunas únicos
    dados_aba.columns = make_unique_columns(dados_aba.columns)



    # Adicionar coluna com o nome do arquivo
    # dados_aba['nome_arquivo_origem'] = arquivo_excel

    # Adicionar os dados da aba ao DataFrame combinado
    df_combined = pd.concat([df_combined, dados_aba], ignore_index=True, sort=False)

# # Ordenar as colunas pelo nome
df_combined = df_combined.sort_index(axis=1)

# Salvar o DataFrame combinado em um novo arquivo Excel na pasta de saída
caminho_saida_arquivo = os.path.join(pasta_saida, "dados_combinados.xlsx")
df_combined.to_excel(caminho_saida_arquivo, index=False)

print(f"Arquivo '{caminho_saida_arquivo}' salvo com sucesso!")
