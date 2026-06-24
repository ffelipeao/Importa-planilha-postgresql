"""Interface de linha de comando para geração de SQL."""

import argparse
import datetime as dt_module

import tkinter as tk
from tkinter import filedialog

from sql_generator.encoding import resolver_codificacao
from sql_generator.orchestrator import SqlGenerationOrchestrator
from sql_generator.prompts import (
    perguntar_codificacao,
    perguntar_modo_tipos,
    perguntar_schema,
    perguntar_validacao_completa,
)


def main():
    """Função principal para gerar CREATE e INSERTs."""
    parser = argparse.ArgumentParser(
        description="Gera scripts SQL (CREATE TABLE + INSERT) a partir de planilhas Excel ou CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python gera_create_inserts.py                              # Seleção interativa (UTF-8)
  python gera_create_inserts.py --codificacao utf-8          # CSV em UTF-8
  python gera_create_inserts.py -c 2                         # CSV em ISO-8859-1 (Latin-1)
  python gera_create_inserts.py -c windows-1252              # CSV em Windows-1252
  python gera_create_inserts.py --inferir-tipos              # Inferir tipos no CREATE TABLE
  python gera_create_inserts.py --validacao-completa         # Validação completa (mais lenta)
  python gera_create_inserts.py --perguntar-tipos            # Escolher modo de tipos interativamente
  python gera_create_inserts.py -s dados_gts                 # Schema sem prompt interativo

Codificações aceitas:
  1 ou utf-8          UTF-8 (padrão)
  2 ou iso-8859-1     ISO-8859-1 (Latin-1)
  3 ou windows-1252   Windows-1252
  ou qualquer nome de codificação suportado pelo Python
        """
    )

    parser.add_argument(
        '-c', '--codificacao',
        type=str,
        default='utf-8',
        metavar='CODIFICACAO',
        help='Codificação para leitura de arquivos CSV (padrão: utf-8). '
             'Atalhos: 1=utf-8, 2=iso-8859-1, 3=windows-1252'
    )

    parser.add_argument(
        '--perguntar-codificacao',
        action='store_true',
        help='Solicita interativamente a codificação dos arquivos CSV'
    )

    parser.add_argument(
        '--inferir-tipos',
        action='store_true',
        help='Infere automaticamente os tipos PostgreSQL das colunas no CREATE TABLE'
    )

    parser.add_argument(
        '--perguntar-tipos',
        action='store_true',
        help='Solicita interativamente o modo de tipos das colunas (text ou inferência)'
    )

    parser.add_argument(
        '--validacao-completa',
        action='store_true',
        help='Valida tipos inferidos em todas as colunas e linhas (mais lenta, mais segura)'
    )

    parser.add_argument(
        '--perguntar-validacao',
        action='store_true',
        help='Solicita interativamente o modo de validação dos tipos inferidos'
    )

    parser.add_argument(
        '-s', '--schema',
        type=str,
        default=None,
        metavar='SCHEMA',
        help='Schema PostgreSQL de destino (se omitido, será solicitado interativamente)'
    )

    args = parser.parse_args()
    if args.perguntar_codificacao:
        codificacao = perguntar_codificacao()
    else:
        codificacao = resolver_codificacao(args.codificacao)

    if args.perguntar_tipos:
        inferir_tipos = perguntar_modo_tipos()
    else:
        inferir_tipos = args.inferir_tipos or args.validacao_completa

    if inferir_tipos and args.perguntar_validacao:
        validacao_completa = perguntar_validacao_completa()
    else:
        validacao_completa = args.validacao_completa

    if args.schema:
        nome_schema = args.schema
    else:
        nome_schema = perguntar_schema()

    hora_inicio = dt_module.datetime.now()
    print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
    root = tk.Tk()
    root.withdraw()
    file_list = filedialog.askopenfilenames(
        title="Selecionar arquivos Excel ou CSV",
        filetypes=[
            ("Arquivos Excel", "*.xlsx"),
            ("Arquivos CSV", "*.csv"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if file_list:
        print('Gerando dados para o schema:', nome_schema)

        orchestrator = SqlGenerationOrchestrator(
            nome_schema,
            codificacao,
            inferir_tipos,
            validacao_completa,
        )
        orchestrator.processar_arquivos(list(file_list))

        print('Gerado com sucesso!!!')
        hora_fim = dt_module.datetime.now()
        duracao_total = hora_fim - hora_inicio

        print("Hora inicial:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
        print("Hora final:", hora_fim.strftime("%Y-%m-%d %H:%M:%S"))
        print("Tempo total de execução:", duracao_total)
    else:
        print("Nenhum arquivo selecionado.")
