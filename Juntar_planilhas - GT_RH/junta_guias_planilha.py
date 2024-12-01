import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

"""
    Felipe Alves - 20241105
    Adaptado para combinar colunas similares sem excluir nenhuma coluna, sem pular as primeiras linhas
    e sem preencher valores vazios com zeros.

    O script faz a leitura de cada aba (guia) das planilhas e combina os dados das colunas de mesmo nome.
    A saída é salva na mesma pasta do arquivo de entrada.

    Entrada: Permite a seleção de várias planilhas no mesmo formato.
    Saída: Para cada planilha lida, gera uma nova com as abas consolidadas.
"""

# Criar uma janela oculta para usar o askopenfilenames
Tk().withdraw()

# Selecionar os arquivos .xlsx (o usuário pode selecionar múltiplos)
arquivos_excel = askopenfilenames(title="Selecione os arquivos .xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])

# Verificar se o usuário selecionou algum arquivo
if not arquivos_excel:
    print("Nenhum arquivo selecionado. O programa será encerrado.")
    exit()

# Processar cada arquivo .xlsx selecionado
for caminho_arquivo in arquivos_excel:
    # Extrair o nome do arquivo e o diretório de entrada
    arquivo_excel = os.path.basename(caminho_arquivo)
    pasta_entrada = os.path.dirname(caminho_arquivo)
    print(f"Processando o arquivo: {arquivo_excel}")

    # Carregar todas as abas em um dicionário (sem pular linhas)
    dados_abas = pd.read_excel(caminho_arquivo, sheet_name=None)

    # Lista para armazenar os DataFrames de cada aba
    dados_combinados_lista = []

    for nome_aba, df in dados_abas.items():
        # Ignorar abas específicas
        if nome_aba in ['Cronograma', 'Planilha1']:
            continue

        # Adicionar coluna com o nome da aba e arquivo de origem
        df['nome_aba'] = nome_aba
        df['nome_arquivo_origem'] = arquivo_excel

        # Adicionar o DataFrame à lista
        dados_combinados_lista.append(df)

    # Combinar todos os DataFrames em um único DataFrame
    df_combined = pd.concat(dados_combinados_lista, ignore_index=True, sort=False)

    # Agrupar colunas semelhantes preservando valores NaN
    df_combined = df_combined.groupby(df_combined.columns, axis=1).apply(
        lambda x: x.bfill(axis=0).ffill(axis=0) if x.isnull().all().any() else x
    )

    # Trabalha o nome do arquivo de saída
    part_n = arquivo_excel.split('.')
    nome_arquivo_saida = f"{part_n[0]}_combinado.{part_n[1]}"

    # Salvar o DataFrame combinado na mesma pasta de entrada
    caminho_saida_arquivo = os.path.join(pasta_entrada, nome_arquivo_saida)
    df_combined.to_excel(caminho_saida_arquivo, index=False)

    print(f"Arquivo '{caminho_saida_arquivo}' salvo com sucesso!")
