"""Enums de domínio para geração de SQL."""

from enum import Enum


class CategoriaValor(Enum):
    """Categoria inferida de um valor de célula."""

    INTEIRO = 'inteiro'
    DECIMAL = 'decimal'
    DATA = 'data'
    TIMESTAMP = 'timestamp'
    BOOLEANO = 'booleano'
    TEXTO = 'texto'
