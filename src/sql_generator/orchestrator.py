"""Orquestração do fluxo de geração de SQL."""

import os
from typing import List, Optional

from executa_arquivo_sql import execute_sql_file

from sql_generator.column_normalizer import ColumnNameNormalizer
from sql_generator.create_table_generator import CreateTableGenerator
from sql_generator.insert_generator import InsertGenerator
from sql_generator.spreadsheet_reader import SpreadsheetReader
from sql_generator.type_inferencer import TypeInferencer
from sql_generator.value_utils import format_file_name


class SqlGenerationOrchestrator:
    """Coordena leitura, inferência de tipos e geração de arquivos SQL."""

    def __init__(
        self,
        nome_schema: str,
        codificacao: str = 'utf-8',
        inferir_tipos: bool = False,
        validacao_completa: bool = False,
    ):
        self.nome_schema = nome_schema
        self.codificacao = codificacao
        self.inferir_tipos = inferir_tipos
        self.validacao_completa = validacao_completa
        self.reader = SpreadsheetReader(codificacao)

    @staticmethod
    def escrever_arquivo_sql(caminho_arquivo: str, conteudo: str) -> bool:
        """Grava o arquivo SQL, substituindo o conteúdo caso o arquivo já exista."""
        pasta_destino = os.path.dirname(caminho_arquivo)
        if pasta_destino:
            os.makedirs(pasta_destino, exist_ok=True)

        arquivo_existia = os.path.exists(caminho_arquivo)
        if arquivo_existia:
            print(f'Arquivo existente encontrado: {caminho_arquivo} — será substituído.')

        with open(caminho_arquivo, 'w', encoding='utf-8') as sql_file:
            sql_file.write(conteudo)

        return arquivo_existia

    def processar_arquivo(self, nome_arquivo: str) -> None:
        try:
            print('Preparando dados do arquivo:', nome_arquivo)
            print('Codificação selecionada:', self.codificacao)
            if self.inferir_tipos:
                if self.validacao_completa:
                    print(
                        'Modo de tipos: inferência com validação completa '
                        '(uma passagem por todas as colunas e linhas)'
                    )
                else:
                    print(
                        'Modo de tipos: inferência rápida '
                        '(amostra na memória + ajuste de VARCHAR em uma passagem)'
                    )
            else:
                print('Modo de tipos: text (padrão)')

            tipos_colunas = None

            print('Carregando dados na memória (df).')
            df = self.reader.ler_arquivo(nome_arquivo, self.codificacao)

            print('Gerando dados para importa...')
            nome_arquivo_base = os.path.basename(nome_arquivo)
            nome_tabela = nome_arquivo_base.rsplit('.', 1)[0].lower()
            nome_tabela_formatado = format_file_name(nome_tabela)

            colunas = ColumnNameNormalizer.normalizar_colunas(df.columns.tolist())
            df.columns = colunas

            if self.inferir_tipos and not self.validacao_completa:
                print('Coletando amostra para inferência de tipos (na memória)...')
                df_amostra = SpreadsheetReader.extrair_amostra_do_dataframe(df)
                tipos_colunas = TypeInferencer.inferir_tipos_colunas(df_amostra, colunas)
                print('Tipos inferidos na amostra:')
                for coluna in colunas:
                    print(f'  - {coluna}: {tipos_colunas[coluna]}')

            if self.inferir_tipos and self.validacao_completa:
                print(
                    'Validação completa de tipos (uma passagem pelo arquivo)...'
                )
                tipos_colunas = TypeInferencer.validar_tipos_pelo_dataset_completo(
                    df, colunas, tipos_colunas
                )
                print('Tipos finais para CREATE TABLE:')
                for coluna in colunas:
                    print(f'  - {coluna}: {tipos_colunas[coluna]}')
            elif self.inferir_tipos and tipos_colunas is not None:
                print('Ajustando tamanhos VARCHAR (uma passagem pelo arquivo)...')
                tipos_colunas = TypeInferencer.ajustar_tipos_pelo_dataset_completo(
                    df, tipos_colunas
                )
                print('Tipos finais para CREATE TABLE:')
                for coluna in colunas:
                    print(f'  - {coluna}: {tipos_colunas[coluna]}')

            print('Gerando CREATE TABLE...')
            create_sql = CreateTableGenerator.gerar(
                self.nome_schema,
                nome_tabela_formatado,
                colunas,
                tipos_colunas,
            )

            print('Gerando INSERT com os dados...')
            insert_sql = InsertGenerator.gerar(
                self.nome_schema,
                nome_tabela_formatado,
                df,
                colunas,
                tipos_colunas,
                usar_texto_para_todos=not self.inferir_tipos,
            )

            print("Escrevendo arquivo .sql")
            caminho_sql = f'sql/{nome_tabela}.sql'
            conteudo_sql = create_sql + '\n' + insert_sql
            arquivo_substituido = self.escrever_arquivo_sql(caminho_sql, conteudo_sql)

            if arquivo_substituido:
                print(f'O arquivo SQL "{nome_tabela}.sql" foi substituído com sucesso para {nome_arquivo}.')
            else:
                print(f'O arquivo SQL "{nome_tabela}.sql" foi criado com sucesso para {nome_arquivo}.')

            print('###' * 50)
            print('###' * 15, "Inserindo no Banco de dados", '###' * 15)
            print('    Executando script sql: ', nome_tabela + '.sql')
            if execute_sql_file('sql/' + nome_tabela + '.sql'):
                print('    Inserido com Sucesso!')
            else:
                print(f'    Erro ao inserir os dados do arquivo sql/{nome_tabela}.sql ')
            print('###' * 50)

        except Exception as e:
            print(f'Erro ao criar o arquivo SQL:', e)

    def processar_arquivos(self, file_list: List[str]) -> None:
        if self.validacao_completa:
            self.inferir_tipos = True

        for nome_arquivo in file_list:
            self.processar_arquivo(nome_arquivo)


def escrever_arquivo_sql(caminho_arquivo: str, conteudo: str) -> bool:
    return SqlGenerationOrchestrator.escrever_arquivo_sql(caminho_arquivo, conteudo)


def gerar_sql(
    file_list,
    nome_schema,
    codificacao='utf-8',
    inferir_tipos=False,
    validacao_completa=False,
):
    orchestrator = SqlGenerationOrchestrator(
        nome_schema,
        codificacao,
        inferir_tipos,
        validacao_completa,
    )
    orchestrator.processar_arquivos(list(file_list))
