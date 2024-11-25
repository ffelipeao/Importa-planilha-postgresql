import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

class ConexaoBanco:
    def __init__(self):
        # Carregar variáveis de ambiente do arquivo .env
        load_dotenv(find_dotenv())

        # Por padrão se conecta no servidor passado com os menos usuário e senha.
        self.server = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.senha = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = os.getenv("DB_PORT")
    def conectar(self):
        try:
            # Conectar ao banco de dados
            conexao = psycopg2.connect(
                dbname=self.database,
                user=self.user,
                password=self.senha,
                host=self.server,
                port=self.port,
                application_name="API_Python"
            )
            # print("Conexão bem-sucedida!")
            return conexao
        except psycopg2.Error as e:
            print("Erro ao conectar:", e)
            return None

    def execute_query(self, conexao, query, parametros=None):
        try:
            cursor = conexao.cursor()
            # Executando a query com os parâmetros passados
            cursor.execute(query, parametros)
            # Se for uma consulta SELECT, obtém os resultados
            if query.strip().upper().startswith("SELECT"):
                # print('Executando SELECT')
                resultados = cursor.fetchall()  # Obtém todos os resultados
                return resultados
            else:
                # Se não for SELECT, faz commit da transação (INSERT, UPDATE, DELETE)
                conexao.commit()
                return True
        except Exception as e:
            msg = f"Erro Query: {e}"
            print(msg)
            return False
        finally:
            cursor.close()  # Garantir que o cursor seja fechado após o uso
