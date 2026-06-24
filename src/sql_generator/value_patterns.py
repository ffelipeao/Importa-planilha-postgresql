"""Padrões e validadores para datas, timestamps, números e booleanos."""

import re
from datetime import datetime

from sql_generator.constants import PADROES_DATA, PADROES_TIMESTAMP, VALORES_BOOLEANOS


def corresponde_inteiro(texto: str) -> bool:
    return bool(re.fullmatch(r'[+-]?\d+', texto))


def corresponde_decimal(texto: str) -> bool:
    return bool(
        re.fullmatch(r'[+-]?\d+[.,]\d+', texto)
        or re.fullmatch(r'[+-]?\d+\.\d+e[+-]?\d+', texto, flags=re.IGNORECASE)
    )


def _data_valida(texto: str) -> bool:
    formatos = ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d')
    for formato in formatos:
        try:
            datetime.strptime(texto, formato)
            return True
        except ValueError:
            continue
    return False


def _timestamp_valido(texto: str) -> bool:
    candidatos = (
        texto,
        texto.replace('T', ' ').replace('Z', ''),
    )
    formatos = (
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%d/%m/%Y %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
    )
    for candidato in candidatos:
        for formato in formatos:
            try:
                datetime.strptime(candidato, formato)
                return True
            except ValueError:
                continue
    return False


def corresponde_data(texto: str) -> bool:
    if any(padrao.match(texto) for padrao in PADROES_DATA):
        return _data_valida(texto)
    return False


def corresponde_timestamp(texto: str) -> bool:
    if any(padrao.match(texto) for padrao in PADROES_TIMESTAMP):
        return _timestamp_valido(texto)
    return False


def corresponde_booleano(texto: str) -> bool:
    return texto.strip().lower() in VALORES_BOOLEANOS
