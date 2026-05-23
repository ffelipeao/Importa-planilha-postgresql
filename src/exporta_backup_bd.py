"""
Script para exportar dump do PostgreSQL e gerenciar backups locais.
Usa a classe ConexaoBanco para obter as credenciais e pg_dump para o backup.
Backups salvos em backup_bd_flonaca/; backups com mais de 15 dias são removidos.
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

from dotenv import load_dotenv, find_dotenv

from conexao import ConexaoBanco


PASTA_BACKUP = "backup_bd_flonaca"


def obter_credenciais():
    """Obtém credenciais do banco a partir da classe ConexaoBanco."""
    load_dotenv(find_dotenv())
    conn = ConexaoBanco()
    return {
        "host": conn.server,
        "port": conn.port or "5432",
        "user": conn.user,
        "password": conn.senha,
        "dbname": conn.database,
    }


def garantir_pasta_backup():
    """Cria a pasta de backup se não existir. Retorna o caminho absoluto."""
    path = Path(PASTA_BACKUP)
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def exportar_dump():
    """
    Exporta um dump do banco PostgreSQL usando pg_dump.
    O arquivo é salvo em backup_bd_flonaca/ com nome contendo data e hora.
    Retorna o caminho do arquivo criado ou None em caso de erro.
    """
    cred = obter_credenciais()
    pasta = garantir_pasta_backup()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"backup_flonaca_{timestamp}.dump"
    caminho_backup = pasta / nome_arquivo

    env = os.environ.copy()
    env["PGPASSWORD"] = cred["password"]

    # As opções de formato são: p (plain SQL), c (custom), t (tar), f (custom format)
    # O formato custom é o mais recomendado para backups de banco de dados.
    # Para .dump, use o formato c.

    cmd = [
        "pg_dump",
        "-h", cred["host"],
        "-p", str(cred["port"]),
        "-U", cred["user"],
        "-d", cred["dbname"],
        "-F", "c",   # formato custom (binário .dump, restaura com pg_restore)
        "-f", str(caminho_backup),
    ]

    try:
        subprocess.run(
            cmd,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Backup exportado com sucesso: {caminho_backup}")
        return str(caminho_backup)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao exportar dump: {e.stderr or e}")
        return None
    except FileNotFoundError:
        print(
            "Erro: pg_dump não encontrado. "
            "Certifique-se de que o PostgreSQL client (binários) está no PATH."
        )
        return None


def validar_e_limpar_backups_antigos(dias=15):
    """
    Valida a data dos backups na pasta backup_bd_flonaca e remove
    os arquivos com mais de `dias` dias.
    Retorna a quantidade de arquivos removidos.
    """
    pasta = Path(PASTA_BACKUP)
    if not pasta.exists():
        print(f"Pasta {PASTA_BACKUP} não existe. Nada a limpar.")
        return 0

    limite = datetime.now() - timedelta(days=dias)
    removidos = 0

    for arquivo in pasta.glob("*.dump"):
        if not arquivo.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(arquivo.stat().st_mtime)
            if mtime < limite:
                arquivo.unlink()
                print(f"Backup antigo removido ({mtime.date()}): {arquivo.name}")
                removidos += 1
        except OSError as e:
            print(f"Erro ao processar {arquivo.name}: {e}")

    if removidos == 0:
        print(f"Nenhum backup com mais de {dias} dias encontrado.")
    else:
        print(f"Total de backups removidos: {removidos}")

    return removidos


def main():
    """Ponto de entrada para CLI e para `poetry run exporta-backup-bd`."""
    print("Iniciando exportação do dump...")
    exportar_dump()
    print("\nVerificando backups antigos (mais de 15 dias)...")
    validar_e_limpar_backups_antigos(15)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
