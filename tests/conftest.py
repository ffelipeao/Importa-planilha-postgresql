"""Fixtures compartilhadas para testes de geração de SQL."""

import csv
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def tmp_csv(tmp_path: Path) -> Path:
    """Cria CSV de exemplo com delimitador ponto-e-vírgula."""
    arquivo = tmp_path / "dados_exemplo.csv"
    linhas = [
        ["ID", "Nome Completo", "Valor", "Ativo", "Data Nasc"],
        ["1", "João Silva", "10,5", "sim", "01/01/1990"],
        ["2", "Maria Souza", "20", "nao", "1990-05-15"],
        ["3", "Empresa XYZ", "abc", "1", "15/03/2020"],
    ]
    with open(arquivo, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(linhas)
    return arquivo


@pytest.fixture
def tmp_xlsx(tmp_path: Path) -> Path:
    """Cria planilha XLSX de exemplo."""
    arquivo = tmp_path / "dados_exemplo.xlsx"
    df = pd.DataFrame(
        {
            "ID": [1, 2, 3],
            "Nome Completo": ["João Silva", "Maria Souza", "Empresa XYZ"],
            "Valor": [10.5, 20, "abc"],
            "Ativo": ["sim", "nao", "1"],
            "Data Nasc": ["01/01/1990", "1990-05-15", "15/03/2020"],
        }
    )
    df.to_excel(arquivo, index=False, engine="openpyxl")
    return arquivo


@pytest.fixture
def colunas_normalizadas():
    return ["id", "nome_completo", "valor", "ativo", "data_nasc"]
