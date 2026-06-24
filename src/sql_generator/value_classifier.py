"""Classificação de valores para inferência de tipos PostgreSQL."""

from datetime import date, datetime

import pandas as pd

from sql_generator.enums import CategoriaValor
from sql_generator.value_patterns import (
    corresponde_booleano,
    corresponde_data,
    corresponde_decimal,
    corresponde_inteiro,
    corresponde_timestamp,
)
from sql_generator.value_utils import valor_para_texto


def classificar_valor(valor) -> CategoriaValor:
    """Classifica um valor em categoria de tipo PostgreSQL."""
    if isinstance(valor, bool):
        return CategoriaValor.BOOLEANO
    if isinstance(valor, datetime):
        if (
            valor.hour == 0
            and valor.minute == 0
            and valor.second == 0
            and valor.microsecond == 0
        ):
            return CategoriaValor.DATA
        return CategoriaValor.TIMESTAMP
    if isinstance(valor, date):
        return CategoriaValor.DATA
    if isinstance(valor, int) and not isinstance(valor, bool):
        return CategoriaValor.INTEIRO
    if isinstance(valor, float):
        if pd.isna(valor):
            return CategoriaValor.TEXTO
        if valor.is_integer():
            return CategoriaValor.INTEIRO
        return CategoriaValor.DECIMAL

    texto = valor_para_texto(valor)
    if not texto:
        return CategoriaValor.TEXTO

    if corresponde_booleano(texto):
        return CategoriaValor.BOOLEANO
    if corresponde_inteiro(texto):
        return CategoriaValor.INTEIRO
    if corresponde_decimal(texto):
        return CategoriaValor.DECIMAL
    if corresponde_timestamp(texto):
        return CategoriaValor.TIMESTAMP
    if corresponde_data(texto):
        return CategoriaValor.DATA
    return CategoriaValor.TEXTO
