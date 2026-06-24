"""Testes de compatibilidade com o módulo legado gera_create_inserts."""

import gera_create_inserts as legacy


def test_reexportacoes_publicas():
    assert legacy.gerar_create_table is not None
    assert legacy.gerar_insert_sql is not None
    assert legacy.ler_arquivo is not None
    assert legacy.inferir_tipos_colunas is not None
    assert legacy.CategoriaValor is not None


def test_normalizar_coluna_via_modulo_legado():
    assert legacy.normalizar_nome_coluna("Código Item") == "codigo_item"
