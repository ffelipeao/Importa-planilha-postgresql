import os
import subprocess
import tempfile
from conexao import ConexaoBanco
from tkinter import Tk, filedialog, simpledialog
import re

# === CONFIGURAÇÕES ===
ESQUEMA = "rasters"
SRID = 4674

def selecionar_pasta():
    Tk().withdraw()
    return filedialog.askdirectory(title="Selecione a pasta com os arquivos TIFF")

def perguntar_gt_origem():
    Tk().withdraw()
    return simpledialog.askstring("GT Correspondente", "Infome o GT:")


def modificar_sql_inserts(sql_original, filename, gt_origem):
    filename = filename.replace("'", "''")
    gt_origem = gt_origem.replace("'", "''")

    linhas_modificadas = []
    for linha in sql_original.splitlines():
        if linha.strip().upper().startswith("INSERT INTO"):
            # Ajustar colunas
            linha_mod = linha.replace('("rast")', "(rast, filename, gt_origem)")

            # Substituir o final de VALUES (...) corretamente
            pos_values = linha_mod.upper().find("VALUES (")
            if pos_values == -1:
                linhas_modificadas.append(linha)  # Linha não é um INSERT válido
                continue

            # Separar antes e depois do VALUES (
            antes = linha_mod[:pos_values + len("VALUES (")]
            dentro = linha_mod[pos_values + len("VALUES ("):].rstrip("); \n")
            linha_final = f"{antes}{dentro}, '{filename}', '{gt_origem}');"

            linhas_modificadas.append(linha_final)
        else:
            linhas_modificadas.append(linha)
    return "\n".join(linhas_modificadas)

def modificar_create_table(sql, filename_col="filename", gt_col="gt_origem"):
    padrao = r'(CREATE\s+TABLE\s+".+?"\s*\()(.*?)(\);)'
    match = re.search(padrao, sql, flags=re.IGNORECASE | re.DOTALL)

    if not match:
        return sql  # Não encontrou o CREATE TABLE, retorna o original

    antes, colunas, depois = match.groups()

    # Remove espaços e quebras de linha extras
    colunas = colunas.strip()

    # Adiciona as novas colunas ao final
    novas_colunas = colunas
    if not novas_colunas.endswith(","):
        novas_colunas += ","
    novas_colunas += f' "{filename_col}" text, "{gt_col}" text'

    novo_create = f"{antes}{novas_colunas}{depois}"

    return re.sub(padrao, novo_create, sql, flags=re.IGNORECASE | re.DOTALL)


def remover_vacuum(sql):
    linhas = sql.splitlines()
    return "\n".join([l for l in linhas if not l.strip().upper().startswith("VACUUM")])

def importar_rasters(pasta_rasters, gt_origem):
    banco = ConexaoBanco()
    conexao = banco.conectar()

    if conexao is None:
        print("❌ Não foi possível conectar ao banco.")
        return

    for root, _, arquivos in os.walk(pasta_rasters):
        for arquivo in arquivos:
            if arquivo.lower().endswith(".tif"):
                caminho_arquivo = os.path.join(root, arquivo)
                print(f"📂 Importando: {caminho_arquivo}")

                try:
                    nome_tabela = os.path.splitext(arquivo)[0].lower()
                    comando = [
                        "raster2pgsql",
                        "-s", str(SRID),
                        "-I",  # <- cria tabela e índice
                        "-M",
                        caminho_arquivo,
                        f"{ESQUEMA}.{nome_tabela}"
                    ]

                    resultado = subprocess.run(
                        comando,
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    sql_cru = resultado.stdout

                    # Adiciona colunas no CREATE TABLE
                    sql_cru = modificar_create_table(sql_cru)

                    # Adiciona valores no INSERT
                    sql_modificado = modificar_sql_inserts(
                        sql_cru,
                        filename=arquivo.lower(),
                        gt_origem=gt_origem
                    )

                    sql_modificado = remover_vacuum(sql_modificado)

                    # print('sadasdasdasdasda')
                    # print(sql_modificado)
                    # exit()

                    with tempfile.NamedTemporaryFile("w+", suffix=".sql", delete=False) as tmpfile:
                        tmpfile.write(sql_modificado)
                        tmpfile_path = tmpfile.name

                    with open(tmpfile_path, 'r', encoding='latin1') as sql_file:
                        cursor = conexao.cursor()
                        cursor.execute(sql_file.read())
                        conexao.commit()
                        cursor.close()

                    print("✅ Importado com sucesso!\n")

                except subprocess.CalledProcessError as e:
                    print(f"❌ Erro no raster2pgsql:\n{e.stderr}")
                except Exception as e:
                    print(f"❌ Erro ao executar SQL: {e}")

    conexao.close()
    print("🏁 Processo finalizado.")

if __name__ == "__main__":
    pasta = selecionar_pasta()
    if not pasta:
        print("❌ Nenhuma pasta selecionada.")
        exit()

    gt_origem = perguntar_gt_origem()
    if not gt_origem:
        print("❌ Nenhum GT informado.")
        exit()

    importar_rasters(pasta, gt_origem)
