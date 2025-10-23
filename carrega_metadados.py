import pandas as pd
from conexao import ConexaoBanco
import datetime
import os
import sys
import argparse
from pathlib import Path

# Tenta importar tkinter, mas não falha se não estiver disponível
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("Aviso: tkinter não está disponível. Use --arquivo para especificar o arquivo.")

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

def selecionar_arquivo_grafico():
    """Seleciona arquivo usando interface gráfica (tkinter)"""
    if not TKINTER_AVAILABLE:
        return None
    
    try:
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        
        # Verifica se está em ambiente headless
        if os.environ.get('DISPLAY') is None and os.environ.get('WAYLAND_DISPLAY') is None:
            print("Aviso: Ambiente headless detectado. Interface gráfica não disponível.")
            root.destroy()
            return None
        
        file_list = filedialog.askopenfilenames(
            title="Selecione a planilha de metadados",
            filetypes=[
                ("Arquivos Excel", "*.xlsx *.xls"),
                ("Arquivos CSV", "*.csv"),
                ("Todos os arquivos", "*.*")
            ]
        )
        root.destroy()
        
        return file_list[0] if file_list else None
        
    except Exception as e:
        print(f"Erro ao abrir interface gráfica: {e}")
        return None

def selecionar_arquivo_interativo():
    """Seleciona arquivo de forma interativa via terminal"""
    print("\nSeleção de arquivo interativa:")
    print("Digite o caminho completo do arquivo ou pressione Enter para cancelar:")
    
    arquivo = input("Caminho do arquivo: ").strip()
    
    if not arquivo:
        return None
    
    # Expande ~ para o diretório home
    arquivo = os.path.expanduser(arquivo)
    
    if not os.path.exists(arquivo):
        print(f"Erro: Arquivo não encontrado: {arquivo}")
        return None
    
    if not os.path.isfile(arquivo):
        print(f"Erro: Caminho não é um arquivo: {arquivo}")
        return None
    
    return arquivo

def buscar_arquivos_excel(diretorio="."):
    """Busca arquivos Excel no diretório atual"""
    extensoes = ['.xlsx', '.xls', '.csv']
    arquivos_encontrados = []
    
    diretorio_path = Path(diretorio)
    
    for extensao in extensoes:
        arquivos_encontrados.extend(diretorio_path.glob(f"*{extensao}"))
    
    return arquivos_encontrados

def selecionar_arquivo_automatico():
    """Tenta encontrar arquivos Excel automaticamente"""
    arquivos = buscar_arquivos_excel()
    
    if not arquivos:
        return None
    
    if len(arquivos) == 1:
        print(f"Arquivo encontrado automaticamente: {arquivos[0]}")
        return str(arquivos[0])
    
    print("\nMúltiplos arquivos encontrados:")
    for i, arquivo in enumerate(arquivos, 1):
        print(f"{i}. {arquivo}")
    
    while True:
        try:
            escolha = input(f"\nEscolha um arquivo (1-{len(arquivos)}) ou 0 para cancelar: ")
            escolha_num = int(escolha)
            
            if escolha_num == 0:
                return None
            
            if 1 <= escolha_num <= len(arquivos):
                return str(arquivos[escolha_num - 1])
            
            print("Escolha inválida. Tente novamente.")
            
        except ValueError:
            print("Digite um número válido.")

def coletar_mudancas_tabelas(cursor, df):
    """Coleta todas as mudanças de comentários de tabelas"""
    mudancas_tabelas = []
    tabelas_ja_processadas = set()
    
    for idx, row in df.iterrows():
        schema = limpar_string(row['schema'])
        tabela = limpar_string(row['tabela'])
        comentario_tabela = limpar_string(row['comentario_tabela'])
        
        if comentario_valido(comentario_tabela):
            chave_tabela = f"{schema}.{tabela}"
            
            if chave_tabela not in tabelas_ja_processadas:
                if verificar_tabela_existe(cursor, schema, tabela):
                    comentario_atual = obter_comentario_tabela(cursor, schema, tabela)
                    
                    if comentario_atual != comentario_tabela:
                        mudancas_tabelas.append({
                            'schema': schema,
                            'tabela': tabela,
                            'comentario_atual': comentario_atual,
                            'comentario_novo': comentario_tabela,
                            'linha': idx + 1
                        })
                
                tabelas_ja_processadas.add(chave_tabela)
    
    return mudancas_tabelas

def coletar_mudancas_colunas(cursor, df):
    """Coleta todas as mudanças de comentários de colunas"""
    mudancas_colunas = []
    
    for idx, row in df.iterrows():
        schema = limpar_string(row['schema'])
        tabela = limpar_string(row['tabela'])
        coluna = limpar_string(row['coluna'])
        comentario_coluna = limpar_string(row['comentario_coluna'])
        
        if comentario_valido(comentario_coluna) and coluna:
            if verificar_coluna_existe(cursor, schema, tabela, coluna):
                comentario_atual = obter_comentario_coluna(cursor, schema, tabela, coluna)
                
                if comentario_atual != comentario_coluna:
                    mudancas_colunas.append({
                        'schema': schema,
                        'tabela': tabela,
                        'coluna': coluna,
                        'comentario_atual': comentario_atual,
                        'comentario_novo': comentario_coluna,
                        'linha': idx + 1
                    })
    
    return mudancas_colunas

def mostrar_previa_mudancas(mudancas_tabelas, mudancas_colunas):
    """Mostra uma prévia das mudanças que serão feitas"""
    print("\n" + "=" * 80)
    print("PRÉ-VISUALIZAÇÃO DAS MUDANÇAS")
    print("=" * 80)
    
    if not mudancas_tabelas and not mudancas_colunas:
        print("✓ Nenhuma mudança será feita - todos os comentários já estão atualizados!")
        return True
    
    # Mostrar mudanças de tabelas
    if mudancas_tabelas:
        print(f"\n📋 TABELAS QUE SERÃO ATUALIZADAS ({len(mudancas_tabelas)}):")
        print("-" * 80)
        
        for i, mudanca in enumerate(mudancas_tabelas, 1):
            print(f"\n{i}. {mudanca['schema']}.{mudanca['tabela']} (linha {mudanca['linha']})")
            print("   ATUAL:")
            if mudanca['comentario_atual']:
                print(f"   '{mudanca['comentario_atual']}'")
            else:
                print("   (sem comentário)")
            print("   NOVO:")
            print(f"   '{mudanca['comentario_novo']}'")
            print("-" * 40)
    
    # Mostrar mudanças de colunas
    if mudancas_colunas:
        print(f"\n📝 COLUNAS QUE SERÃO ATUALIZADAS ({len(mudancas_colunas)}):")
        print("-" * 80)
        
        for i, mudanca in enumerate(mudancas_colunas, 1):
            print(f"\n{i}. {mudanca['schema']}.{mudanca['tabela']}.{mudanca['coluna']} (linha {mudanca['linha']})")
            print("   ATUAL:")
            if mudanca['comentario_atual']:
                print(f"   '{mudanca['comentario_atual']}'")
            else:
                print("   (sem comentário)")
            print("   NOVO:")
            print(f"   '{mudanca['comentario_novo']}'")
            print("-" * 40)
    
    print("\n" + "=" * 80)
    return False

def confirmar_execucao():
    """Solicita confirmação do usuário para executar as mudanças"""
    print("\n🤔 Deseja executar essas mudanças?")
    print("Digite:")
    print("  's' ou 'sim' - Para executar as mudanças")
    print("  'n' ou 'não' - Para cancelar")
    print("  'dry' - Para simular sem executar")
    
    while True:
        resposta = input("\nSua escolha: ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            return 'executar'
        elif resposta in ['n', 'não', 'nao', 'no']:
            return 'cancelar'
        elif resposta == 'dry':
            return 'dry_run'
        else:
            print("Resposta inválida. Digite 's' para sim, 'n' para não, ou 'dry' para simular.")

def executar_mudancas(cursor, mudancas_tabelas, mudancas_colunas, dry_run=False):
    """Executa as mudanças no banco de dados"""
    if dry_run:
        print("\n🔍 MODO SIMULAÇÃO - Nenhuma mudança será feita no banco")
    
    tabelas_atualizadas = 0
    colunas_atualizadas = 0
    
    # Executar mudanças de tabelas
    for mudanca in mudancas_tabelas:
        if not dry_run:
            atualizar_comentario_tabela(
                cursor, 
                mudanca['schema'], 
                mudanca['tabela'], 
                mudanca['comentario_novo']
            )
        print(f"  ✓ Tabela {mudanca['schema']}.{mudanca['tabela']} {'atualizada' if not dry_run else '(simulado)'}")
        tabelas_atualizadas += 1
    
    # Executar mudanças de colunas
    for mudanca in mudancas_colunas:
        if not dry_run:
            atualizar_comentario_coluna(
                cursor, 
                mudanca['schema'], 
                mudanca['tabela'], 
                mudanca['coluna'], 
                mudanca['comentario_novo']
            )
        print(f"  ✓ Coluna {mudanca['schema']}.{mudanca['tabela']}.{mudanca['coluna']} {'atualizada' if not dry_run else '(simulado)'}")
        colunas_atualizadas += 1
    
    return tabelas_atualizadas, colunas_atualizadas

def obter_arquivo_planilha(arquivo_especificado=None):
    """Obtém o arquivo da planilha usando diferentes métodos"""
    
    # Se arquivo foi especificado via linha de comando
    if arquivo_especificado:
        arquivo_path = Path(arquivo_especificado)
        
        if not arquivo_path.exists():
            print(f"Erro: Arquivo não encontrado: {arquivo_especificado}")
            return None
        
        if not arquivo_path.is_file():
            print(f"Erro: Caminho não é um arquivo: {arquivo_especificado}")
            return None
        
        print(f"Usando arquivo especificado: {arquivo_path}")
        return str(arquivo_path)
    
    # Tenta interface gráfica primeiro
    if TKINTER_AVAILABLE:
        print("Tentando abrir interface gráfica...")
        arquivo = selecionar_arquivo_grafico()
        if arquivo:
            return arquivo
    
    # Se interface gráfica falhou ou não está disponível
    print("\nInterface gráfica não disponível. Tentando métodos alternativos...")
    
    # Tenta encontrar arquivos automaticamente
    arquivo = selecionar_arquivo_automatico()
    if arquivo:
        return arquivo
    
    # Como último recurso, usa entrada interativa
    return selecionar_arquivo_interativo()

def main():
    """Função principal do programa"""
    # Configura argumentos de linha de comando
    parser = argparse.ArgumentParser(
        description="Carrega metadados de planilhas para PostgreSQL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python carrega_metadados.py                           # Seleção interativa com confirmação
  python carrega_metadados.py --arquivo dados.xlsx      # Arquivo específico
  python carrega_metadados.py --dry-run                 # Simula mudanças sem executar
  python carrega_metadados.py --auto-confirm            # Executa sem pedir confirmação
  python carrega_metadados.py -a dados.csv --dry-run    # Combina arquivo + simulação
        """
    )
    
    parser.add_argument(
        '-a', '--arquivo',
        type=str,
        help='Caminho para o arquivo da planilha (Excel ou CSV)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simula as mudanças sem executá-las no banco'
    )
    
    parser.add_argument(
        '--auto-confirm',
        action='store_true',
        help='Executa automaticamente sem pedir confirmação (use com cuidado!)'
    )
    
    parser.add_argument(
        '--versao',
        action='version',
        version='Carregador de Metadados v2.0'
    )
    
    args = parser.parse_args()
    
    # Registra o horário de início
    hora_inicio = datetime.datetime.now()
    print("=" * 60)
    print("CARREGAMENTO DE METADADOS - PostgreSQL")
    print("=" * 60)
    print(f"Hora inicial: {hora_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conecta ao banco
    print("Conectando ao banco de dados...")
    conn = ConexaoBanco().conectar()
    if not conn:
        print("\n" + "=" * 60)
        print("ERRO: Não foi possível conectar ao banco de dados!")
        print("=" * 60)
        print("\nPara resolver este problema:")
        print("1. Verifique se o PostgreSQL está rodando")
        print("2. Crie um arquivo .env na raiz do projeto com as configurações do banco")
        print("3. Use o arquivo 'env_exemplo.txt' como modelo")
        print("4. Verifique se as credenciais estão corretas")
        print("\nExemplo de arquivo .env:")
        print("DB_HOST=localhost")
        print("DB_PORT=5432")
        print("DB_NAME=seu_banco")
        print("DB_USER=seu_usuario")
        print("DB_PASSWORD=sua_senha")
        print("\n" + "=" * 60)
        return 1
    
    cursor = conn.cursor()
    
    # Seleciona o arquivo
    print("\nSelecionando arquivo da planilha...")
    arquivo_selecionado = obter_arquivo_planilha(args.arquivo)
    
    if not arquivo_selecionado:
        print("Nenhum arquivo selecionado. Encerrando...")
        cursor.close()
        conn.close()
        return 0

    try:
        # Lê a planilha
        print(f"Carregando arquivo: {arquivo_selecionado}")
        
        # Detecta o tipo de arquivo e lê adequadamente
        arquivo_path = Path(arquivo_selecionado)
        extensao = arquivo_path.suffix.lower()
        
        if extensao in ['.xlsx', '.xls']:
            df = pd.read_excel(arquivo_selecionado)
        elif extensao == '.csv':
            df = pd.read_csv(arquivo_selecionado)
        else:
            print(f"Erro: Formato de arquivo não suportado: {extensao}")
            print("Formatos suportados: .xlsx, .xls, .csv")
            cursor.close()
            conn.close()
            return 1
        
        print(f"Arquivo carregado com sucesso!")
        print(f"Total de registros: {len(df)}")
        print(f"Colunas encontradas: {list(df.columns)}")
        print("-" * 60)
        
        # Verifica se as colunas necessárias existem
        colunas_necessarias = ['schema', 'tabela', 'comentario_tabela', 'coluna', 'comentario_coluna']
        colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
        
        if colunas_faltantes:
            print(f"ERRO: Colunas faltantes na planilha: {colunas_faltantes}")
            print(f"Colunas disponíveis: {list(df.columns)}")
            cursor.close()
            conn.close()
            return 1
        
        # Coleta todas as mudanças que serão feitas
        print("\nAnalisando mudanças necessárias...")
        mudancas_tabelas = coletar_mudancas_tabelas(cursor, df)
        mudancas_colunas = coletar_mudancas_colunas(cursor, df)
        
        # Mostra pré-visualização das mudanças
        sem_mudancas = mostrar_previa_mudancas(mudancas_tabelas, mudancas_colunas)
        
        if sem_mudancas:
            print("\n✓ Processamento concluído - nenhuma mudança necessária!")
            return 0
        
        # Determina a ação baseada nos argumentos
        if args.dry_run:
            acao = 'dry_run'
            print("\n🔍 Modo dry-run ativado via linha de comando")
        elif args.auto_confirm:
            acao = 'executar'
            print("\n⚡ Auto-confirmação ativada - executando mudanças automaticamente")
        else:
            # Solicita confirmação do usuário
            acao = confirmar_execucao()
            
            if acao == 'cancelar':
                print("\n❌ Operação cancelada pelo usuário.")
                return 0
        
        # Executa as mudanças
        dry_run = (acao == 'dry_run')
        print(f"\n{'🔍 Simulando' if dry_run else '⚡ Executando'} mudanças...")
        
        tabelas_atualizadas, colunas_atualizadas = executar_mudancas(
            cursor, mudancas_tabelas, mudancas_colunas, dry_run
        )
        
        # Confirma as alterações (apenas se não for dry run)
        if not dry_run:
            conn.commit()
            print(f"\n✓ {tabelas_atualizadas} tabelas e {colunas_atualizadas} colunas atualizadas com sucesso!")
        else:
            print(f"\n🔍 Simulação concluída: {tabelas_atualizadas} tabelas e {colunas_atualizadas} colunas seriam atualizadas")
        
        # Relatório final
        hora_fim = datetime.datetime.now()
        tempo_total = hora_fim - hora_inicio
        
        print("\n" + "=" * 60)
        print("RELATÓRIO FINAL")
        print("=" * 60)
        print(f"Hora final: {hora_fim.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tempo total: {tempo_total}")
        print("-" * 60)
        print(f"TABELAS {'SIMULADAS' if dry_run else 'ATUALIZADAS'}: {tabelas_atualizadas}")
        print(f"COLUNAS {'SIMULADAS' if dry_run else 'ATUALIZADAS'}: {colunas_atualizadas}")
        print("-" * 60)
        
        if dry_run:
            print("🔍 MODO SIMULAÇÃO - Nenhuma alteração foi feita no banco")
        else:
            print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        
        print("=" * 60)
        
        return 0

    except Exception as e:
        print(f"\nERRO durante o processamento: {e}")
        conn.rollback()
        return 1
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    sys.exit(main())