import os
import pandas as pd
import psycopg2
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
import re

def criar_tabela_postgresql_com_nome_arquivo(nome_arquivo, db_params):
    """Cria uma tabela PostgreSQL a partir de uma planilha"""
    try:
        # Determinar o tipo de arquivo usando a extensão
        extensao = os.path.splitext(nome_arquivo)[1]

        # Ler o arquivo usando Pandas dependendo do tipo
        if extensao.lower() == '.xlsx':
            df = pd.read_excel(nome_arquivo)
        elif extensao.lower() == '.csv':
            df = pd.read_csv(nome_arquivo)
        else:
            return "Formato de arquivo não suportado."

        # Extrair o nome do arquivo (sem a extensão) para usar como nome da tabela
        nome_arquivo_base = os.path.basename(nome_arquivo)
        nome_tabela = nome_arquivo_base.split('.')[0]

        # Substituir caracteres não-alfabéticos nos nomes das colunas
        df.columns = [re.sub(r'[^a-zA-Z0-9]', '', col) for col in df.columns]

        # Criar uma string com a instrução SQL CREATE
        create_sql = f"CREATE TABLE {nome_tabela} ({', '.join([f'{col} text' for col in df.columns])})"
        
        # Imprimir a instrução SQL CREATE na tela
        print("Instrução SQL CREATE:")
        print(create_sql)

        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Criar uma tabela no PostgreSQL com os mesmos nomes das colunas no DataFrame
        cur.execute(create_sql)
        conn.commit()

        # Inserir os dados do DataFrame na tabela do PostgreSQL
        df.to_sql(nome_tabela, conn, if_exists='replace', index=False)

        # Fechar a conexão com o banco de dados
        conn.close()

        return f"Tabela '{nome_tabela}' criada com sucesso no PostgreSQL."
    except Exception as e:
        return f"Erro ao criar a tabela: {str(e)}"

def main():
    """Função principal para importação básica"""
    print("📊 IMPORTAR PLANILHA PARA POSTGRESQL")
    print("-" * 50)
    
    # Carregar variáveis de ambiente a partir do arquivo .env
    load_dotenv()

    # Usar as variáveis de ambiente
    db_params = {
        'dbname': os.getenv('DB_NAME', default='seu_banco_de_dados'),
        'user': os.getenv('DB_USER', default='seu_usuario'),
        'password': os.getenv('DB_PASSWORD', default='sua_senha'),
        'host': os.getenv('DB_HOST', default='localhost'),
        'port': os.getenv('DB_PORT', default='5432')
    }

    # Criar uma janela de diálogo para selecionar o arquivo
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    nome_arquivo = filedialog.askopenfilename(
        title="Selecionar planilha para importar",
        filetypes=[
            ("Arquivos Excel", "*.xlsx"),
            ("Arquivos CSV", "*.csv"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if nome_arquivo:
        print(f"Arquivo selecionado: {nome_arquivo}")
        print("Processando...")
        
        # Chamar a função para criar a tabela no PostgreSQL
        resultado = criar_tabela_postgresql_com_nome_arquivo(nome_arquivo, db_params)

        # Exibir o resultado
        print("\n" + "=" * 50)
        print(resultado)
        print("=" * 50)
    else:
        print("❌ Nenhum arquivo selecionado.")

if __name__ == "__main__":
    main()
