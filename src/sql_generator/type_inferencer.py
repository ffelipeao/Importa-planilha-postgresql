"""Inferência de tipos PostgreSQL a partir de dados de planilha."""

import re
from typing import Dict, Optional, Sequence, Set

import pandas as pd

from sql_generator.constants import (
    INT32_MAX,
    INT32_MIN,
    LIMITE_CARACTERES_TEXTO,
    VALORES_BOOLEANOS,
    VARCHAR_MARGEM_SEGURANCA,
    VARCHAR_TAMANHO_MINIMO,
)
from sql_generator.enums import CategoriaValor
from sql_generator.models import EstadoInferenciaColuna
from sql_generator.value_classifier import classificar_valor
from sql_generator.value_utils import (
    tamanho_maximo_amostra,
    valor_para_texto,
    valor_vazio,
    valores_contem_texto_nao_numerico,
)


class TypeInferencer:
    """Infere tipos PostgreSQL para colunas de planilhas."""

    @staticmethod
    def coluna_exige_integer_por_nome(nome_coluna: str) -> bool:
        return nome_coluna == 'id' or nome_coluna.startswith('id_')

    @staticmethod
    def arredondar_tamanho_varchar(tamanho: int) -> int:
        """Arredonda VARCHAR para a dezena superior; abaixo de 10 mantém o valor exato."""
        tamanho = max(tamanho, VARCHAR_TAMANHO_MINIMO)
        if tamanho < 10:
            return tamanho
        return ((tamanho + 9) // 10) * 10

    @classmethod
    def calcular_tipo_cadeia_por_tamanho(cls, tamanho_maximo: int) -> str:
        if tamanho_maximo > LIMITE_CARACTERES_TEXTO:
            return 'text'
        tamanho = max(tamanho_maximo + VARCHAR_MARGEM_SEGURANCA, VARCHAR_TAMANHO_MINIMO)
        if tamanho > LIMITE_CARACTERES_TEXTO:
            return 'text'
        tamanho = cls.arredondar_tamanho_varchar(tamanho)
        tamanho = min(tamanho, LIMITE_CARACTERES_TEXTO)
        return f'varchar({tamanho})'

    @classmethod
    def inferir_varchar(cls, valores: Sequence, tamanho_maximo: Optional[int] = None) -> str:
        if tamanho_maximo is None:
            tamanho_maximo = tamanho_maximo_amostra(valores)
        return cls.calcular_tipo_cadeia_por_tamanho(tamanho_maximo)

    @classmethod
    def tipo_inteiro_por_magnitude(cls, valores: Sequence) -> str:
        for valor in valores:
            if valor_vazio(valor):
                continue
            if isinstance(valor, bool):
                continue
            try:
                if isinstance(valor, int):
                    numero = valor
                elif isinstance(valor, float):
                    numero = int(valor)
                else:
                    numero = int(valor_para_texto(valor))
            except (ValueError, TypeError, OverflowError):
                return cls.inferir_varchar(valores)
            if numero < INT32_MIN or numero > INT32_MAX:
                return 'bigint'
        return 'integer'

    @staticmethod
    def tipo_eh_cadeia_curta(tipo_coluna: str) -> bool:
        return bool(re.fullmatch(r'varchar\(\d+\)', tipo_coluna, flags=re.IGNORECASE))

    @staticmethod
    def combinar_categorias(categorias: Set[CategoriaValor]) -> str:
        if not categorias or categorias == {CategoriaValor.TEXTO}:
            return 'varchar'

        if CategoriaValor.TEXTO in categorias:
            return 'varchar'

        if CategoriaValor.BOOLEANO in categorias:
            if categorias == {CategoriaValor.BOOLEANO}:
                return 'boolean'
            return 'varchar'

        if CategoriaValor.TIMESTAMP in categorias:
            if categorias <= {CategoriaValor.TIMESTAMP, CategoriaValor.DATA}:
                return 'timestamp'
            return 'varchar'

        if CategoriaValor.DATA in categorias:
            if categorias == {CategoriaValor.DATA}:
                return 'date'
            if categorias <= {CategoriaValor.DATA, CategoriaValor.TIMESTAMP}:
                return 'timestamp'
            return 'varchar'

        if CategoriaValor.DECIMAL in categorias:
            if categorias <= {CategoriaValor.DECIMAL, CategoriaValor.INTEIRO}:
                return 'numeric'
            return 'varchar'

        if categorias == {CategoriaValor.INTEIRO}:
            return 'integer'

        return 'varchar'

    @classmethod
    def finalizar_tipo_coluna(cls, estado: EstadoInferenciaColuna) -> str:
        """Define o tipo PostgreSQL a partir do estado acumulado da coluna."""
        if estado.texto_longo:
            return 'text'
        if estado.quantidade_validos == 0:
            return cls.calcular_tipo_cadeia_por_tamanho(0)

        if cls.coluna_exige_integer_por_nome(estado.nome_coluna):
            if not estado.tem_texto_nao_numerico and estado.categorias == {CategoriaValor.INTEIRO}:
                return 'bigint' if estado.exige_bigint else 'integer'

        categorias = set(estado.categorias)
        if CategoriaValor.BOOLEANO in categorias:
            if not estado.textos_validos.issubset(VALORES_BOOLEANOS):
                categorias.discard(CategoriaValor.BOOLEANO)
                if not categorias:
                    return cls.calcular_tipo_cadeia_por_tamanho(estado.tamanho_maximo)

        tipo = cls.combinar_categorias(categorias)
        if tipo == 'integer':
            return 'bigint' if estado.exige_bigint else 'integer'
        if tipo == 'varchar':
            return cls.calcular_tipo_cadeia_por_tamanho(estado.tamanho_maximo)
        return tipo

    @classmethod
    def inferir_tipo_coluna(cls, nome_coluna: str, valores: Sequence) -> str:
        valores_validos = []
        for valor in valores:
            if valor_vazio(valor):
                continue
            texto = valor_para_texto(valor)
            if len(texto) > LIMITE_CARACTERES_TEXTO:
                return 'text'
            valores_validos.append(valor)

        if not valores_validos:
            return cls.inferir_varchar(valores_validos)

        if cls.coluna_exige_integer_por_nome(nome_coluna):
            if not valores_contem_texto_nao_numerico(valores_validos):
                tipo_inteiro = cls.tipo_inteiro_por_magnitude(valores_validos)
                if tipo_inteiro in ('integer', 'bigint'):
                    return tipo_inteiro

        categorias = {classificar_valor(valor) for valor in valores_validos}

        if CategoriaValor.BOOLEANO in categorias:
            textos = {valor_para_texto(valor).lower() for valor in valores_validos}
            if not textos.issubset(VALORES_BOOLEANOS):
                categorias.discard(CategoriaValor.BOOLEANO)
                if not categorias:
                    return cls.inferir_varchar(valores_validos)

        tipo = cls.combinar_categorias(categorias)
        if tipo == 'integer':
            return cls.tipo_inteiro_por_magnitude(valores_validos)
        if tipo == 'varchar':
            return cls.inferir_varchar(valores_validos)
        return tipo

    @classmethod
    def inferir_tipos_colunas(cls, df_amostra: pd.DataFrame, colunas: Sequence[str]) -> Dict[str, str]:
        tipos = {}
        for coluna in colunas:
            valores = df_amostra[coluna].tolist() if coluna in df_amostra.columns else []
            tipos[coluna] = cls.inferir_tipo_coluna(coluna, valores)
        return tipos

    @classmethod
    def inferir_tipo_coluna_completo(cls, df: pd.DataFrame, nome_coluna: str) -> str:
        """Inferência de uma coluna com saída antecipada para valores longos."""
        if nome_coluna not in df.columns:
            return cls.calcular_tipo_cadeia_por_tamanho(0)

        estado = EstadoInferenciaColuna(nome_coluna)
        for valor in df[nome_coluna].to_numpy():
            estado.processar_valor(valor)
            if estado.concluida():
                break
        return cls.finalizar_tipo_coluna(estado)

    @classmethod
    def ajustar_tipos_pelo_dataset_completo(
        cls,
        df: pd.DataFrame,
        tipos_colunas: Dict[str, str],
    ) -> Dict[str, str]:
        """Recalcula VARCHAR/text em uma única passagem pelas linhas do DataFrame."""
        colunas_varchar = [
            coluna for coluna, tipo in tipos_colunas.items()
            if cls.tipo_eh_cadeia_curta(tipo) and coluna in df.columns
        ]
        if not colunas_varchar:
            return dict(tipos_colunas)

        tamanhos_maximos = {coluna: 0 for coluna in colunas_varchar}
        excedeu_limite = {coluna: False for coluna in colunas_varchar}

        for linha in df[colunas_varchar].to_numpy():
            for indice, valor in enumerate(linha):
                coluna = colunas_varchar[indice]
                if excedeu_limite[coluna] or valor_vazio(valor):
                    continue
                tamanho = len(valor_para_texto(valor))
                if tamanho > LIMITE_CARACTERES_TEXTO:
                    excedeu_limite[coluna] = True
                elif tamanho > tamanhos_maximos[coluna]:
                    tamanhos_maximos[coluna] = tamanho

        tipos_ajustados = dict(tipos_colunas)
        for coluna in colunas_varchar:
            if excedeu_limite[coluna]:
                tamanho_maximo = LIMITE_CARACTERES_TEXTO + 1
            else:
                tamanho_maximo = tamanhos_maximos[coluna]
            tipo = tipos_colunas[coluna]
            tipo_ajustado = cls.calcular_tipo_cadeia_por_tamanho(tamanho_maximo)
            if tipo_ajustado != tipo:
                print(
                    f'  - {coluna}: {tipo} -> {tipo_ajustado} '
                    f'(tamanho máximo no arquivo: {tamanho_maximo})'
                )
            tipos_ajustados[coluna] = tipo_ajustado
        return tipos_ajustados

    @classmethod
    def validar_tipos_pelo_dataset_completo(
        cls,
        df: pd.DataFrame,
        colunas: Sequence[str],
        tipos_referencia: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """Reinfere tipos de todas as colunas em uma única passagem pelas linhas."""
        colunas_analise = [coluna for coluna in colunas if coluna in df.columns]
        estados = {coluna: EstadoInferenciaColuna(coluna) for coluna in colunas_analise}
        total_linhas = len(df)
        total_colunas = len(colunas)

        if colunas_analise:
            for indice_linha, linha in enumerate(df[colunas_analise].to_numpy(), start=1):
                for indice_coluna, valor in enumerate(linha):
                    estado = estados[colunas_analise[indice_coluna]]
                    if not estado.concluida():
                        estado.processar_valor(valor)

                if total_linhas >= 1000 and indice_linha % 1000 == 0:
                    print(f'  Progresso: {indice_linha}/{total_linhas} linhas analisadas')

        tipos_validados = {}
        for indice, coluna in enumerate(colunas, start=1):
            estado = estados.get(coluna)
            if estado is None:
                tipo_novo = cls.calcular_tipo_cadeia_por_tamanho(0)
            else:
                tipo_novo = cls.finalizar_tipo_coluna(estado)

            tipo_anterior = tipos_referencia.get(coluna) if tipos_referencia else None
            if tipo_anterior and tipo_anterior != tipo_novo:
                print(f'  - {coluna}: {tipo_anterior} -> {tipo_novo}')
            tipos_validados[coluna] = tipo_novo

            if total_colunas >= 20 and (indice % 20 == 0 or indice == total_colunas):
                print(f'  Progresso da validação completa: {indice}/{total_colunas} colunas')

        return tipos_validados


def coluna_exige_integer_por_nome(nome_coluna: str) -> bool:
    return TypeInferencer.coluna_exige_integer_por_nome(nome_coluna)


def tipo_inteiro_por_magnitude(valores: Sequence) -> str:
    return TypeInferencer.tipo_inteiro_por_magnitude(valores)


def inferir_varchar(valores: Sequence, tamanho_maximo: Optional[int] = None) -> str:
    return TypeInferencer.inferir_varchar(valores, tamanho_maximo)


def arredondar_tamanho_varchar(tamanho: int) -> int:
    return TypeInferencer.arredondar_tamanho_varchar(tamanho)


def calcular_tipo_cadeia_por_tamanho(tamanho_maximo: int) -> str:
    return TypeInferencer.calcular_tipo_cadeia_por_tamanho(tamanho_maximo)


def finalizar_tipo_coluna(estado: EstadoInferenciaColuna) -> str:
    return TypeInferencer.finalizar_tipo_coluna(estado)


def inferir_tipo_coluna_completo(df: pd.DataFrame, nome_coluna: str) -> str:
    return TypeInferencer.inferir_tipo_coluna_completo(df, nome_coluna)


def ajustar_tipos_pelo_dataset_completo(
    df: pd.DataFrame,
    tipos_colunas: Dict[str, str],
) -> Dict[str, str]:
    return TypeInferencer.ajustar_tipos_pelo_dataset_completo(df, tipos_colunas)


def validar_tipos_pelo_dataset_completo(
    df: pd.DataFrame,
    colunas: Sequence[str],
    tipos_referencia: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    return TypeInferencer.validar_tipos_pelo_dataset_completo(df, colunas, tipos_referencia)


def tipo_eh_cadeia_curta(tipo_coluna: str) -> bool:
    return TypeInferencer.tipo_eh_cadeia_curta(tipo_coluna)


def combinar_categorias(categorias: Set[CategoriaValor]) -> str:
    return TypeInferencer.combinar_categorias(categorias)


def inferir_tipo_coluna(nome_coluna: str, valores: Sequence) -> str:
    return TypeInferencer.inferir_tipo_coluna(nome_coluna, valores)


def inferir_tipos_colunas(df_amostra: pd.DataFrame, colunas: Sequence[str]) -> Dict[str, str]:
    return TypeInferencer.inferir_tipos_colunas(df_amostra, colunas)
