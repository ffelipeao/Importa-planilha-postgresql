"""Testes de leitura de planilhas CSV e XLSX."""

import pandas as pd

from sql_generator.spreadsheet_reader import SpreadsheetReader, ler_arquivo


def test_ler_csv(tmp_csv):
    df = ler_arquivo(str(tmp_csv), codificacao="utf-8")
    assert len(df) == 3
    assert list(df.columns) == ["ID", "Nome Completo", "Valor", "Ativo", "Data Nasc"]


def test_ler_xlsx(tmp_xlsx):
    df = ler_arquivo(str(tmp_xlsx))
    assert len(df) == 3
    assert "Nome Completo" in df.columns


def test_contar_linhas_csv(tmp_csv):
    reader = SpreadsheetReader("utf-8")
    assert reader.contar_linhas_csv(str(tmp_csv), "utf-8") == 3


def test_ler_cabecalho_csv(tmp_csv):
    reader = SpreadsheetReader("utf-8")
    cabecalho = reader.ler_cabecalho_csv(str(tmp_csv), "utf-8")
    assert cabecalho[0] == "ID"


def test_ler_amostra_para_inferencia_csv(tmp_csv):
    reader = SpreadsheetReader("utf-8")
    df_amostra, colunas = reader.ler_amostra_para_inferencia(str(tmp_csv))
    assert isinstance(df_amostra, pd.DataFrame)
    assert colunas == ["id", "nome_completo", "valor", "ativo", "data_nasc"]


def test_ler_amostra_para_inferencia_xlsx(tmp_xlsx):
    reader = SpreadsheetReader("utf-8")
    df_amostra, colunas = reader.ler_amostra_para_inferencia(str(tmp_xlsx))
    assert len(colunas) == 5
    assert "id" in colunas
