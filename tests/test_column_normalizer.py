"""Testes de normalização de nomes de colunas."""

from sql_generator.column_normalizer import ColumnNameNormalizer, normalizar_colunas, normalizar_nome_coluna


def test_normalizar_nome_coluna_remove_acentos_e_espacos():
    assert normalizar_nome_coluna("Nome Completo") == "nome_completo"
    assert normalizar_nome_coluna("Código") == "codigo"


def test_normalizar_nome_coluna_prefixa_digitos():
    assert normalizar_nome_coluna("123abc") == "col_123abc"


def test_normalizar_nome_coluna_vazio_usa_padrao():
    assert normalizar_nome_coluna("!!!") == "coluna"


def test_normalizar_colunas_resolve_duplicatas():
    colunas = ColumnNameNormalizer.normalizar_colunas(["ID", "id", "Id"])
    assert colunas == ["id", "id_1", "id_2"]


def test_compatibilidade_funcoes_modulo():
    assert normalizar_colunas(["A", "A"]) == ["a", "a_1"]
