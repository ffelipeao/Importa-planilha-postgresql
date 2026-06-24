"""Utilitários para tratamento de strings, valores nulos e identificadores SQL."""

import re
from typing import Sequence

import pandas as pd
import unidecode

from sql_generator.value_patterns import corresponde_decimal, corresponde_inteiro


def format_file_name(file_name: str) -> str:
    """Normaliza nome de arquivo/tabela removendo acentos e espaços."""
    formatted_name = unidecode.unidecode(str(file_name))
    formatted_name = re.sub(r'\s+', ' ', formatted_name).strip()
    formatted_name = formatted_name.replace(' ', '_')
    formatted_name = re.sub(r'_{2,}', '_', formatted_name)
    formatted_name = formatted_name.strip('_')
    return formatted_name


def sanitizar_identificador(identificador: str) -> str:
    """Remove caracteres inválidos e normaliza espaços/underscores em identificadores SQL."""
    nome = format_file_name(identificador)
    nome = re.sub(r'[^a-zA-Z0-9_]', '', nome)
    nome = re.sub(r'_{2,}', '_', nome).strip('_')
    return nome


def tratar_dado(dado) -> str:
    """Escapa aspas simples e remove caracteres indesejados para SQL."""
    if isinstance(dado, str):
        dado_tratado = dado.replace("_x000D_", "").replace("'", "''").replace(" ", "")
    elif isinstance(dado, float):
        if dado.is_integer():
            dado_tratado = str(int(dado))
        else:
            dado_tratado = str(dado)
    else:
        dado_tratado = str(dado)
    return dado_tratado


def valor_vazio(valor) -> bool:
    """Indica se o valor deve ser tratado como NULL no SQL."""
    if valor is None or pd.isna(valor):
        return True
    if isinstance(valor, str) and not valor.strip():
        return True
    return False


def valor_para_texto(valor) -> str:
    """Converte valor de célula para representação textual padronizada."""
    from datetime import date, datetime

    if isinstance(valor, datetime):
        return valor.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(valor, date):
        return valor.strftime('%Y-%m-%d')
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor).strip()


def citar_identificador(identificador: str) -> str:
    """Coloca o identificador entre aspas duplas (palavras reservadas do PostgreSQL)."""
    return f'"{identificador}"'


def valores_contem_texto_nao_numerico(valores: Sequence) -> bool:
    for valor in valores:
        if valor_vazio(valor):
            continue
        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            continue
        texto = valor_para_texto(valor)
        if not (corresponde_inteiro(texto) or corresponde_decimal(texto)):
            return True
    return False


def tamanho_maximo_amostra(valores: Sequence) -> int:
    tamanho_maximo = 0
    for valor in valores:
        if valor_vazio(valor):
            continue
        tamanho_maximo = max(tamanho_maximo, len(valor_para_texto(valor)))
    return tamanho_maximo


def coluna_excede_limite_texto(valores: Sequence) -> bool:
    """Verifica se algum valor ultrapassa o limite; interrompe na primeira ocorrência."""
    from sql_generator.constants import LIMITE_CARACTERES_TEXTO

    for valor in valores:
        if valor_vazio(valor):
            continue
        if len(valor_para_texto(valor)) > LIMITE_CARACTERES_TEXTO:
            return True
    return False


def valores_excedem_limite_texto(valores: Sequence) -> bool:
    return coluna_excede_limite_texto(valores)
