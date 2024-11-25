import os
from conexao import ConexaoBanco
from tkinter import filedialog, Tk
import datetime

def execute_sql_file(file_path):
    try:
        conexao = ConexaoBanco().conectar()
        cursor = conexao.cursor()
        with open(file_path, 'r', encoding='utf-8') as sql_file:
            sql = sql_file.read()

        cursor.execute(sql)
        conexao.commit()

        cursor.close()
        conexao.close()

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

    # Define o caminho inicial para a janela de seleção de arquivos
    caminho_inicial = "sql"

    # Abra a janela de seleção de arquivo para escolher os arquivos .sql
    arquivos_sql = filedialog.askopenfilenames(
        filetypes=[("Arquivos SQL", "*.sql")],
        initialdir=caminho_inicial  # Define o diretório inicial
    )

    if arquivos_sql:
        for arquivo_sql in arquivos_sql:
            print('Inserindo dados pelo arquivo:', arquivo_sql)
            execute_sql_file(arquivo_sql)
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