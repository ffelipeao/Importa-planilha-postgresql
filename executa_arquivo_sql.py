import os
import psycopg2
from decouple import config
from tkinter import filedialog, Tk

# Inicialize uma instância do Tkinter para criar uma janela invisível
root = Tk()
root.withdraw()

# Abra a janela de seleção de arquivo para escolher o arquivo .sql
arquivo_sql = filedialog.askopenfilename(
    filetypes=[("Arquivos SQL", "*.sql")]
)

# Certifique-se de que um arquivo .sql foi selecionado
if arquivo_sql:
    # Defina as configurações do banco de dados usando o .env
    db_params = {
        'dbname': config('DB_NAME', default='seu_banco_de_dados'),
        'user': config('DB_USER', default='seu_usuario'),
        'password': config('DB_PASSWORD', default='sua_senha'),
        'host': config('DB_HOST', default='localhost'),
        'port': config('DB_PORT', default='5432')
    }

    try:
        # Conecte-se ao banco de dados usando as configurações do .env
        conn = psycopg2.connect(**db_params)

        # Crie um cursor para executar as instruções SQL
        cursor = conn.cursor()

        # Leia o arquivo SQL selecionado
        with open(arquivo_sql, 'r', encoding='utf-8') as sql_file:
            sql = sql_file.read()

        # Execute as instruções SQL no banco de dados
        cursor.execute(sql)

        # Faça o commit para confirmar as alterações
        conn.commit()

        # Feche o cursor e a conexão
        cursor.close()
        conn.close()

        print('Dados inseridos no banco de dados com sucesso.')
    except Exception as e:
        print(f'Erro ao inserir dados no banco de dados: {str(e)}')
else:
    print('Nenhum arquivo SQL selecionado.')

# Encerre a instância do Tkinter
root.quit()
