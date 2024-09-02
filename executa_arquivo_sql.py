import os
import psycopg2
from dotenv import load_dotenv
from tkinter import filedialog, Tk
import datetime

def execute_sql_file(file_path, db_params):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        with open(file_path, 'r', encoding='utf-8') as sql_file:
            sql = sql_file.read()

        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()

        print(f'Dados do arquivo {file_path} inseridos no banco de dados com sucesso.')
    except Exception as e:
        print(f'Erro ao inserir dados do arquivo {file_path} no banco de dados: {str(e)}')

if __name__ == "__main__":
    # Registra o horário de início
    hora_inicio = datetime.datetime.now()
    print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
    # Inicialize uma instância do Tkinter para criar uma janela invisível
    root = Tk()
    root.withdraw()

    # Abra a janela de seleção de arquivo para escolher os arquivos .sql
    arquivos_sql = filedialog.askopenfilenames(filetypes=[("Arquivos SQL", "*.sql")])

    if arquivos_sql:
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

        for arquivo_sql in arquivos_sql:
            print('Inserindo dados pelo arquivo:', arquivo_sql)
            execute_sql_file(arquivo_sql, db_params)
    else:
        print('Nenhum arquivo SQL selecionado.')

    # Encerre a instância do Tkinter
    root.quit()

    # Registra o horário de término
    hora_fim = datetime.datetime.now()
    # Calcula a duração total
    duracao_total = hora_fim - hora_inicio

    print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
    print("Hora final:", hora_fim.strftime("%Y-%m-%d %H:%M:%S"))
    print("Tempo total de execução:", duracao_total)