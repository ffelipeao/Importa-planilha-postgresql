"""Testes de inferência de tipos PostgreSQL."""

import pandas as pd

from sql_generator.type_inferencer import TypeInferencer, inferir_tipos_colunas


def test_inferir_tipos_colunas_amostra(tmp_csv, colunas_normalizadas):
    df = pd.read_csv(tmp_csv, encoding="utf-8", delimiter=";")
    df.columns = colunas_normalizadas
    tipos = inferir_tipos_colunas(df, colunas_normalizadas)

    assert tipos["id"] == "integer"
    assert tipos["nome_completo"].startswith("varchar")
    assert tipos["valor"].startswith("varchar")
    assert tipos["ativo"] == "boolean"
    assert tipos["data_nasc"] == "date"


def test_calcular_varchar_por_tamanho():
    assert TypeInferencer.calcular_tipo_cadeia_por_tamanho(5) == "varchar(7)"
    assert TypeInferencer.calcular_tipo_cadeia_por_tamanho(60) == "text"


def test_coluna_id_bigint_para_valores_grandes():
    valores = [3_000_000_000]
    assert TypeInferencer.inferir_tipo_coluna("id", valores) == "bigint"
