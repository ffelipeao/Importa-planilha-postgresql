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
            # Verificar se as variáveis de ambiente estão definidas
            if not all([self.server, self.user, self.senha, self.database, self.port]):
                print("ERRO: Variáveis de ambiente do banco não estão definidas!")
                print("Verifique se existe um arquivo .env com as seguintes variáveis:")
                print("  DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT")
                print(f"Valores atuais:")
                print(f"  DB_HOST: {self.server}")
                print(f"  DB_USER: {self.user}")
                print(f"  DB_PASSWORD: {'***' if self.senha else 'NÃO DEFINIDO'}")
                print(f"  DB_NAME: {self.database}")
                print(f"  DB_PORT: {self.port}")
                return None
            
            print(f"Tentando conectar ao banco: {self.server}:{self.port}/{self.database}")
            print(f"Usuário: {self.user}")
            
            # Conectar ao banco de dados com timeout
            conexao = psycopg2.connect(
                dbname=self.database,
                user=self.user,
                password=self.senha,
                host=self.server,
                port=self.port,
                application_name="API_Python",
                connect_timeout=10  # Timeout de 10 segundos
            )
            print("✓ Conexão bem-sucedida!")
            return conexao
        except psycopg2.OperationalError as e:
            print(f"ERRO de conexão: {e}")
            print("\nPossíveis causas:")
            print("1. Banco de dados não está rodando")
            print("2. Credenciais incorretas")
            print("3. Firewall bloqueando a conexão")
            print("4. Host/porta incorretos")
            return None
        except psycopg2.Error as e:
            print(f"ERRO do PostgreSQL: {e}")
            return None
        except Exception as e:
            print(f"ERRO inesperado: {e}")
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
