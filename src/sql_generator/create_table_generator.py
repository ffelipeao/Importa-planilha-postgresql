"""Geração de comandos CREATE TABLE."""

from typing import Dict, Optional, Sequence

from sql_generator.value_utils import citar_identificador


class CreateTableGenerator:
    """Gera DDL CREATE TABLE para PostgreSQL."""

    @staticmethod
    def gerar(
        nome_schema: str,
        nome_tabela: str,
        colunas: Sequence[str],
        tipos_colunas: Optional[Dict[str, str]] = None,
    ) -> str:
        definicoes_colunas = []
        for coluna in colunas:
            tipo = tipos_colunas.get(coluna, 'text') if tipos_colunas else 'text'
            definicoes_colunas.append(f'{citar_identificador(coluna)} {tipo}')
        colunas_sql = ', '.join(definicoes_colunas)
        return (
            f'CREATE TABLE {nome_schema}.{citar_identificador(nome_tabela)} '
            f'(_id_origem serial, {colunas_sql});'
        )


def gerar_create_table(
    nome_schema: str,
    nome_tabela: str,
    colunas: Sequence[str],
    tipos_colunas: Optional[Dict[str, str]] = None,
) -> str:
    return CreateTableGenerator.gerar(nome_schema, nome_tabela, colunas, tipos_colunas)
