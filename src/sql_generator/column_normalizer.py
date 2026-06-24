"""Normalização de nomes de colunas para identificadores PostgreSQL."""

from typing import List, Sequence

from sql_generator.value_utils import sanitizar_identificador


class ColumnNameNormalizer:
    """Normaliza nomes de colunas e resolve duplicatas."""

    @staticmethod
    def normalizar_nome_coluna(nome_coluna: str) -> str:
        nome = sanitizar_identificador(str(nome_coluna)).lower()
        if not nome:
            nome = 'coluna'
        if nome[0].isdigit():
            nome = f'col_{nome}'
        return nome

    @classmethod
    def normalizar_colunas(cls, colunas: Sequence[str]) -> List[str]:
        nomes_normalizados = []
        contagem = {}
        for coluna in colunas:
            nome = cls.normalizar_nome_coluna(coluna)
            if nome in contagem:
                contagem[nome] += 1
                nome = f'{nome}_{contagem[nome]}'
            else:
                contagem[nome] = 0
            nomes_normalizados.append(nome)
        return nomes_normalizados


def normalizar_nome_coluna(nome_coluna: str) -> str:
    return ColumnNameNormalizer.normalizar_nome_coluna(nome_coluna)


def normalizar_colunas(colunas: Sequence[str]) -> List[str]:
    return ColumnNameNormalizer.normalizar_colunas(colunas)
