import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory

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

    # Carregar a primeira aba do arquivo Excel, pulando as linhas 2 e 3 (índices 1 e 2)
    # Remover "skiprows=[1, 2]" caso queira pegar todas as linhas
    dados_aba = pd.read_excel(caminho_arquivo, sheet_name=0, skiprows=[1, 2])

    # Tornar os nomes das colunas únicos
    dados_aba.columns = make_unique_columns(dados_aba.columns)

    # Adicionar coluna com o nome do arquivo
    dados_aba['nome_arquivo_origem'] = arquivo_excel

    # Adicionar os dados da aba ao DataFrame combinado
    df_combined = pd.concat([df_combined, dados_aba], ignore_index=True, sort=False)

# # Ordenar as colunas pelo nome
# df_combined = df_combined.sort_index(axis=1)

# Salvar o DataFrame combinado em um novo arquivo Excel na pasta de saída
caminho_saida_arquivo = os.path.join(pasta_saida, "dados_combinados.xlsx")
df_combined.to_excel(caminho_saida_arquivo, index=False)

print(f"Arquivo '{caminho_saida_arquivo}' salvo com sucesso!")
