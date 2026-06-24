"""Utilitários de codificação para leitura de CSV."""

import chardet


def detectar_codificacao(arquivo: str) -> str:
    with open(arquivo, 'rb') as f:
        dados = f.read()
        resultado = chardet.detect(dados)
        return resultado['encoding']


def resolver_codificacao(codific) -> str:
    """Converte atalho numérico ou nome de codificação para o valor usado na leitura do CSV."""
    if codific == '1':
        return 'utf-8'
    if codific == '2':
        return 'iso-8859-1'
    if codific == '3':
        return 'windows-1252'
    return codific
