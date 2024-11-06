import pandas as pd

# Caminho para o arquivo .xlsx
arquivo_excel = '5_3_Dados_Hidroquimicos_Superficiais_SN_Vale_2022.xlsx'

# Carregar todas as abas em um dicionário
# Cada chave será o nome da aba e o valor será o DataFrame com os dados da aba
# Carregar todas as abas em um dicionário, pulando as primeiras 6 linhas (linha 7 = index 6)
dados_abas = pd.read_excel(arquivo_excel, sheet_name=None, skiprows=7)


# Loop para transpor os dados de cada aba
dados_transpostos = {}
for nome_aba, df in dados_abas.items():
    # Pula abas que estavam ocultas no docomentos e não precisam ser transportas.
    if nome_aba == 'Cronograma' or nome_aba == 'Planilha1':
         continue
    #
    # Remover a primeira coluna
    df = df.iloc[:, 1:]

    # print(nome_aba)
    # exit()

    # Preencher valores NaN das células mescladas com o valor anterior da linha
    # df = df.ffill(axis=1)

    # Transpor o DataFrame
    df_transposto = df.T
    # Salvar no dicionário com o nome da aba original
    dados_transpostos[nome_aba] = df_transposto

    # Exibir a transposição (opcional)
    print(f"Dados da aba '{nome_aba}' transpostos:")
    # print(df_transposto)
    # print("\n" + "-"*40 + "\n")
    # exit()


# Se quiser salvar cada aba transposta em um novo arquivo Excel
with pd.ExcelWriter('saidas/'+arquivo_excel) as writer:
    for nome_aba, df_transposto in dados_transpostos.items():
        df_transposto.to_excel(writer, sheet_name=nome_aba)

print("Arquivo 'saidas/arquivo_transposto.xlsx' salvo com sucesso!")
