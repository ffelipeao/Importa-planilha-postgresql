"""Modelos de domínio para inferência de tipos PostgreSQL."""

from typing import Set

from sql_generator.constants import INT32_MAX, INT32_MIN, LIMITE_CARACTERES_TEXTO
from sql_generator.enums import CategoriaValor
from sql_generator.value_classifier import classificar_valor
from sql_generator.value_patterns import corresponde_decimal, corresponde_inteiro
from sql_generator.value_utils import valor_para_texto, valor_vazio


class EstadoInferenciaColuna:
    """Acumula estatísticas de uma coluna em uma única passagem pelos dados."""

    def __init__(self, nome_coluna: str):
        self.nome_coluna = nome_coluna
        self.texto_longo = False
        self.tamanho_maximo = 0
        self.categorias: Set[CategoriaValor] = set()
        self.quantidade_validos = 0
        self.tem_texto_nao_numerico = False
        self.exige_bigint = False
        self.textos_validos: Set[str] = set()

    def processar_valor(self, valor) -> None:
        if self.texto_longo or valor_vazio(valor):
            return

        texto = valor_para_texto(valor)
        tamanho = len(texto)
        if tamanho > LIMITE_CARACTERES_TEXTO:
            self.texto_longo = True
            return

        self.quantidade_validos += 1
        if tamanho > self.tamanho_maximo:
            self.tamanho_maximo = tamanho

        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            if isinstance(valor, int):
                if valor < INT32_MIN or valor > INT32_MAX:
                    self.exige_bigint = True
            elif valor.is_integer():
                numero = int(valor)
                if numero < INT32_MIN or numero > INT32_MAX:
                    self.exige_bigint = True
        elif not (corresponde_inteiro(texto) or corresponde_decimal(texto)):
            self.tem_texto_nao_numerico = True
        elif corresponde_inteiro(texto):
            try:
                numero = int(texto)
                if numero < INT32_MIN or numero > INT32_MAX:
                    self.exige_bigint = True
            except (ValueError, OverflowError):
                self.tem_texto_nao_numerico = True

        self.categorias.add(classificar_valor(valor))
        self.textos_validos.add(texto.lower())

    def concluida(self) -> bool:
        return self.texto_longo
