import pandas as pd
from conexao import ConexaoBanco
import datetime
import tkinter as tk
from tkinter import filedialog

# Criado em 2025-08-15 por Felipe
# Atualizado em 2025-01-XX para trabalhar com campos: schema, tabela, comentario_tabela, coluna, comentario_coluna
# Documentação:
#1 - Ler planilha com campos: schema, tabela, comentario_tabela, coluna, comentario_coluna
#2 - Verificar se as tabelas existem no banco
#3 - Atualizar comentários de tabelas se necessário
#4 - Verificar se as colunas existem no banco
#5 - Atualizar comentários de colunas se necessário
#6 - Gerar relatório detalhado das operações

def limpar_string(valor):
    """Remove aspas duplas, simples e espaços em branco"""
    if pd.isna(valor):
        return None
    return str(valor).strip('"').strip("'").strip()

def comentario_valido(comentario):
    """Verifica se o comentário é válido (não vazio ou nulo)"""
    if pd.isna(comentario) or str(comentario).strip() == '' or str(comentario).lower() == 'nan':
        return False
    return True

def verificar_tabela_existe(cursor, schema, tabela):
    """Verifica se a tabela existe no banco"""
    cursor.execute("""
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = %s
        AND table_name = %s;
    """, (schema, tabela))
    return cursor.fetchone() is not None

def verificar_coluna_existe(cursor, schema, tabela, coluna):
    """Verifica se a coluna existe no banco"""
    cursor.execute("""
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name = %s
        AND lower(column_name) = %s;
    """, (schema, tabela, coluna.lower()))
    return cursor.fetchone() is not None

def obter_comentario_tabela(cursor, schema, tabela):
    """Obtém o comentário atual da tabela"""
    cursor.execute("""
        SELECT d.description
        FROM pg_catalog.pg_description d
        JOIN pg_catalog.pg_class c ON c.oid = d.objoid
        JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = %s
        AND c.relname = %s
        AND d.objsubid = 0;
    """, (schema, tabela))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def obter_comentario_coluna(cursor, schema, tabela, coluna):
    """Obtém o comentário atual da coluna"""
    cursor.execute("""
        SELECT d.description
        FROM pg_catalog.pg_description d
        JOIN pg_catalog.pg_class c ON c.oid = d.objoid
        JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
        JOIN pg_catalog.pg_attribute a ON a.attrelid = c.oid AND a.attnum = d.objsubid
        WHERE n.nspname = %s
        AND c.relname = %s
        AND lower(a.attname) = %s;
    """, (schema, tabela, coluna.lower()))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def atualizar_comentario_tabela(cursor, schema, tabela, comentario):
    """Atualiza o comentário da tabela"""
    cursor.execute(f"""
        COMMENT ON TABLE "{schema}"."{tabela}" IS %s;
    """, (comentario,))

def atualizar_comentario_coluna(cursor, schema, tabela, coluna, comentario):
    """Atualiza o comentário da coluna"""
    cursor.execute(f"""
        COMMENT ON COLUMN "{schema}"."{tabela}"."{coluna}" IS %s;
    """, (comentario,))

# Registra o horário de início
hora_inicio = datetime.datetime.now()
print("=" * 60)
print("CARREGAMENTO DE METADADOS - PostgreSQL")
print("=" * 60)
print(f"Hora inicial: {hora_inicio.strftime('%Y-%m-%d %H:%M:%S')}")

# Conecta ao banco
conn = ConexaoBanco().conectar()
if not conn:
    print("Erro: Não foi possível conectar ao banco de dados!")
    exit(1)

cursor = conn.cursor()

# Seleciona o arquivo
root = tk.Tk()
root.withdraw()
file_list = filedialog.askopenfilenames(filetypes=[("Supported Files", "*.xlsx;*.csv"),])

if not file_list:
    print("Nenhum arquivo selecionado. Encerrando...")
    cursor.close()
    conn.close()
    exit(0)

try:
    # Lê a planilha
    df = pd.read_excel(file_list[0])
    print(f"Arquivo carregado: {file_list[0]}")
    print(f"Total de registros: {len(df)}")
    print(f"Colunas encontradas: {list(df.columns)}")
    print("-" * 60)
    
    # Verifica se as colunas necessárias existem
    colunas_necessarias = ['schema', 'tabela', 'comentario_tabela', 'coluna', 'comentario_coluna']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
    
    if colunas_faltantes:
        print(f"ERRO: Colunas faltantes na planilha: {colunas_faltantes}")
        print(f"Colunas disponíveis: {list(df.columns)}")
        exit(1)
    
    # Contadores para relatório
    tabelas_processadas = 0
    tabelas_atualizadas = 0
    tabelas_nao_encontradas = []
    tabelas_comentario_igual = 0
    
    colunas_processadas = 0
    colunas_atualizadas = 0
    colunas_nao_encontradas = []
    colunas_comentario_igual = 0
    
    # Processa cada linha da planilha
    for idx, row in df.iterrows():
        # Limpa os dados
        schema = limpar_string(row['schema'])
        tabela = limpar_string(row['tabela'])
        comentario_tabela = limpar_string(row['comentario_tabela'])
        coluna = limpar_string(row['coluna'])
        comentario_coluna = limpar_string(row['comentario_coluna'])
        
        # print(f"\nProcessando linha {idx + 1}: {schema}.{tabela}")
        
        # Processa comentário da tabela
        if comentario_valido(comentario_tabela):
            if verificar_tabela_existe(cursor, schema, tabela):
                comentario_atual = obter_comentario_tabela(cursor, schema, tabela)

                # print("--------------------------------")
                # print(comentario_atual)
                # print(comentario_tabela)
                # print("--------------------------------")
                # exit()

                if comentario_atual != comentario_tabela:
                    atualizar_comentario_tabela(cursor, schema, tabela, comentario_tabela)
                    print(f"  ✓ Comentário da tabela atualizado")
                    tabelas_atualizadas += 1
                else:
                    # print(f"  - Comentário da tabela já está atualizado")
                    tabelas_comentario_igual += 1
                tabelas_processadas += 1
            else:
                tabelas_nao_encontradas.append(f"{schema}.{tabela}")
                print(f"  ✗ Tabela não encontrada: {schema}.{tabela}")
        
        # Processa comentário da coluna
        if comentario_valido(comentario_coluna) and coluna:
            if verificar_coluna_existe(cursor, schema, tabela, coluna):
                comentario_atual = obter_comentario_coluna(cursor, schema, tabela, coluna)
                
                if comentario_atual != comentario_coluna:
                    atualizar_comentario_coluna(cursor, schema, tabela, coluna, comentario_coluna)
                    print(f"  ✓ Comentário da coluna '{coluna}' atualizado")
                    colunas_atualizadas += 1
                else:
                    # print(f"  - Comentário da coluna '{coluna}' já está atualizado")
                    colunas_comentario_igual += 1
                colunas_processadas += 1
            else:
                colunas_nao_encontradas.append(f"{schema}.{tabela}.{coluna}")
                print(f"  ✗ Coluna não encontrada: {schema}.{tabela}.{coluna}")
    
    # Confirma as alterações
    conn.commit()
    
    # Relatório final
    hora_fim = datetime.datetime.now()
    tempo_total = hora_fim - hora_inicio
    
    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL")
    print("=" * 60)
    print(f"Hora final: {hora_fim.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Tempo total: {tempo_total}")
    print("-" * 60)
    print("TABELAS:")
    print(f"  Processadas: {tabelas_processadas}")
    print(f"  Atualizadas: {tabelas_atualizadas}")
    print(f"  Já atualizadas: {tabelas_comentario_igual}")
    print(f"  Não encontradas: {len(tabelas_nao_encontradas)}")
    print("-" * 60)
    print("COLUNAS:")
    print(f"  Processadas: {colunas_processadas}")
    print(f"  Atualizadas: {colunas_atualizadas}")
    print(f"  Já atualizadas: {colunas_comentario_igual}")
    print(f"  Não encontradas: {len(colunas_nao_encontradas)}")
    
    if tabelas_nao_encontradas:
        print("\nTABELAS NÃO ENCONTRADAS:")
        for t in tabelas_nao_encontradas:
            print(f"  - {t}")
    
    if colunas_nao_encontradas:
        print("\nCOLUNAS NÃO ENCONTRADAS:")
        for c in colunas_nao_encontradas:
            print(f"  - {c}")
    
    print("\n" + "=" * 60)
    print("PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 60)

except Exception as e:
    print(f"\nERRO durante o processamento: {e}")
    conn.rollback()
    raise
finally:
    cursor.close()
    conn.close()