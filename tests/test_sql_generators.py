"""Testes de geração de CREATE TABLE e INSERT."""

import pandas as pd

from sql_generator.create_table_generator import gerar_create_table
from sql_generator.insert_generator import gerar_insert_sql


def test_gerar_create_table_com_texto(colunas_normalizadas):
    sql = gerar_create_table("dados_gts", "dados_exemplo", colunas_normalizadas)
    assert sql.startswith('CREATE TABLE dados_gts."dados_exemplo"')
    assert '"id" text' in sql
    assert "_id_origem serial" in sql


def test_gerar_create_table_com_tipos(colunas_normalizadas):
    tipos = {
        "id": "integer",
        "nome_completo": "varchar(20)",
        "valor": "numeric",
        "ativo": "boolean",
        "data_nasc": "date",
    }
    sql = gerar_create_table("dados_gts", "dados_exemplo", colunas_normalizadas, tipos)
    assert '"id" integer' in sql
    assert '"ativo" boolean' in sql
    assert '"data_nasc" date' in sql


def test_gerar_insert_sql_modo_texto(tmp_csv, colunas_normalizadas):
    df = pd.read_csv(tmp_csv, encoding="utf-8", delimiter=";")
    df.columns = colunas_normalizadas

    sql = gerar_insert_sql(
        "dados_gts",
        "dados_exemplo",
        df,
        colunas_normalizadas,
        usar_texto_para_todos=True,
    )

    assert sql.startswith('INSERT INTO dados_gts."dados_exemplo"')
    assert "'João Silva'" in sql or "'Jo\u00e3o Silva'" in sql
    assert sql.endswith(";")


def test_gerar_insert_sql_com_tipos_inferidos(tmp_csv, colunas_normalizadas):
    df = pd.read_csv(tmp_csv, encoding="utf-8", delimiter=";")
    df.columns = colunas_normalizadas
    tipos = {
        "id": "integer",
        "nome_completo": "varchar(20)",
        "valor": "varchar(10)",
        "ativo": "boolean",
        "data_nasc": "date",
    }

    sql = gerar_insert_sql(
        "dados_gts",
        "dados_exemplo",
        df,
        colunas_normalizadas,
        tipos,
        usar_texto_para_todos=False,
    )

    assert "1," in sql or "(1," in sql
    assert "true" in sql or "false" in sql
    assert "'1990-05-15'" in sql
    assert sql.endswith(";")
