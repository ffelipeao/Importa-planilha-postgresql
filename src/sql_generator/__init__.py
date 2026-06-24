"""Pacote modular para geração de scripts SQL a partir de planilhas."""

from sql_generator.cli import main
from sql_generator.column_normalizer import ColumnNameNormalizer, normalizar_colunas, normalizar_nome_coluna
from sql_generator.create_table_generator import CreateTableGenerator, gerar_create_table
from sql_generator.encoding import detectar_codificacao, resolver_codificacao
from sql_generator.enums import CategoriaValor
from sql_generator.insert_generator import InsertGenerator, formatar_valor_insert, gerar_insert_sql
from sql_generator.models import EstadoInferenciaColuna
from sql_generator.orchestrator import SqlGenerationOrchestrator, escrever_arquivo_sql, gerar_sql
from sql_generator.spreadsheet_reader import SpreadsheetReader, ler_arquivo
from sql_generator.type_inferencer import TypeInferencer, inferir_tipos_colunas

__all__ = [
    'CategoriaValor',
    'ColumnNameNormalizer',
    'CreateTableGenerator',
    'EstadoInferenciaColuna',
    'InsertGenerator',
    'SpreadsheetReader',
    'SqlGenerationOrchestrator',
    'TypeInferencer',
    'detectar_codificacao',
    'escrever_arquivo_sql',
    'formatar_valor_insert',
    'gerar_create_table',
    'gerar_insert_sql',
    'gerar_sql',
    'inferir_tipos_colunas',
    'ler_arquivo',
    'main',
    'normalizar_colunas',
    'normalizar_nome_coluna',
    'resolver_codificacao',
]
