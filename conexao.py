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
