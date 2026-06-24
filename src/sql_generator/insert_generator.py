"""Geração de comandos INSERT."""

import datetime as dt_module
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Dict, Optional, Sequence

import pandas as pd

from sql_generator.type_inferencer import TypeInferencer
from sql_generator.value_utils import citar_identificador, tratar_dado, valor_para_texto, valor_vazio


class InsertGenerator:
    """Gera comandos INSERT a partir de DataFrames."""

    @staticmethod
    def _converter_booleano_sql(valor) -> str:
        if isinstance(valor, bool):
            return 'true' if valor else 'false'
        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            return 'true' if int(valor) == 1 else 'false'
        texto = valor_para_texto(valor).lower()
        if texto in {'true', 't', 'sim', 'yes', 'y', '1', 's'}:
            return 'true'
        if texto in {'false', 'f', 'nao', 'não', 'no', 'n', '0'}:
            return 'false'
        return f"'{tratar_dado(valor)}'"

    @staticmethod
    def _converter_numero_sql(valor) -> str:
        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            if isinstance(valor, float) and valor.is_integer():
                return str(int(valor))
            return str(valor)
        texto = valor_para_texto(valor).replace(',', '.')
        try:
            numero = Decimal(texto)
        except InvalidOperation:
            return f"'{tratar_dado(valor)}'"
        if numero == numero.to_integral_value():
            return str(int(numero))
        return format(numero.normalize(), 'f').rstrip('0').rstrip('.') or '0'

    @staticmethod
    def _converter_data_sql(valor) -> str:
        if isinstance(valor, datetime):
            return f"'{valor.strftime('%Y-%m-%d')}'"
        if isinstance(valor, date):
            return f"'{valor.strftime('%Y-%m-%d')}'"
        texto = valor_para_texto(valor)
        formatos = ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d')
        for formato in formatos:
            try:
                data = datetime.strptime(texto, formato)
                return f"'{data.strftime('%Y-%m-%d')}'"
            except ValueError:
                continue
        return f"'{tratar_dado(valor)}'"

    @staticmethod
    def _converter_timestamp_sql(valor) -> str:
        if isinstance(valor, datetime):
            return f"'{valor.strftime('%Y-%m-%d %H:%M:%S')}'"
        if isinstance(valor, date):
            return f"'{valor.strftime('%Y-%m-%d')}'"
        texto = valor_para_texto(valor).replace('T', ' ')
        formatos = (
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%d/%m/%Y %H:%M:%S',
            '%d-%m-%Y %H:%M:%S',
        )
        for formato in formatos:
            try:
                data_hora = datetime.strptime(texto, formato)
                return f"'{data_hora.strftime('%Y-%m-%d %H:%M:%S')}'"
            except ValueError:
                continue
        return f"'{tratar_dado(valor)}'"

    @classmethod
    def formatar_valor_insert(
        cls,
        valor,
        tipo_coluna: str,
        usar_texto_para_todos: bool = False,
    ) -> str:
        if valor_vazio(valor):
            return 'NULL'

        if usar_texto_para_todos or tipo_coluna == 'text' or TypeInferencer.tipo_eh_cadeia_curta(tipo_coluna):
            return f"'{tratar_dado(valor)}'"

        if tipo_coluna == 'boolean':
            return cls._converter_booleano_sql(valor)

        if tipo_coluna in ('integer', 'bigint'):
            return cls._converter_numero_sql(valor)

        if tipo_coluna == 'numeric':
            return cls._converter_numero_sql(valor)

        if tipo_coluna == 'date':
            return cls._converter_data_sql(valor)

        if tipo_coluna == 'timestamp':
            return cls._converter_timestamp_sql(valor)

        return f"'{tratar_dado(valor)}'"

    @classmethod
    def gerar(
        cls,
        nome_schema: str,
        nome_tabela: str,
        df: pd.DataFrame,
        colunas: Sequence[str],
        tipos_colunas: Optional[Dict[str, str]] = None,
        usar_texto_para_todos: bool = False,
    ) -> str:
        colunas_sql = ', '.join(citar_identificador(coluna) for coluna in colunas)
        insert_sql = (
            f'INSERT INTO {nome_schema}.{citar_identificador(nome_tabela)} '
            f'({colunas_sql}) VALUES\n'
        )

        total_linhas = df.shape[0]
        print("Total de linhas no DataFrame:", total_linhas)

        conta = 0
        for _, row in df.iterrows():
            conta += 1
            if conta % 25000 == 0:
                porcentagem = round((conta / total_linhas) * 100, 2)
                current_datetime = dt_module.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(
                    'Data e hora:', current_datetime,
                    '| Linhas processadas:', conta, ' - ', porcentagem, "%",
                )

            valores = []
            for coluna in colunas:
                tipo = tipos_colunas.get(coluna, 'text') if tipos_colunas else 'text'
                valores.append(
                    cls.formatar_valor_insert(
                        row[coluna],
                        tipo,
                        usar_texto_para_todos=usar_texto_para_todos,
                    )
                )
            insert_sql += f"({', '.join(valores)}),\n"

        return insert_sql.rstrip(',\n') + ';'


def formatar_valor_insert(
    valor,
    tipo_coluna: str,
    usar_texto_para_todos: bool = False,
) -> str:
    return InsertGenerator.formatar_valor_insert(valor, tipo_coluna, usar_texto_para_todos)


def gerar_insert_sql(
    nome_schema: str,
    nome_tabela: str,
    df: pd.DataFrame,
    colunas: Sequence[str],
    tipos_colunas: Optional[Dict[str, str]] = None,
    usar_texto_para_todos: bool = False,
) -> str:
    return InsertGenerator.gerar(
        nome_schema,
        nome_tabela,
        df,
        colunas,
        tipos_colunas,
        usar_texto_para_todos,
    )
