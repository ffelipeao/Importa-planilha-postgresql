import os
import sys
import subprocess
from dotenv import load_dotenv

def mostrar_menu():
    """Exibe o menu principal do sistema"""
    print("\n" + "=" * 60)
    print("🚀 IMPORTADOR DE PLANILHAS PARA POSTGRESQL")
    print("=" * 60)
    print("Escolha uma opção:")
    print()
    print("1. 📝 Gerenciar Metadados de Tabelas")
    print("2. 📄 Gerar Scripts SQL (CREATE + INSERT)")
    print("3. 🗺️  Dados Geoespaciais")
    print("4. 🛠️  Ferramentas Auxiliares")
    print("5. ❓ Ajuda")
    print("0. 🚪 Sair")
    print("=" * 60)

def executar_metadados():
    """Executa o gerenciamento de metadados"""
    print("\n📝 GERENCIAR METADADOS DE TABELAS")
    print("-" * 40)
    print("Esta função adiciona comentários descritivos em tabelas e colunas")
    print("Suporte a pré-visualização e confirmação de mudanças")
    print()
    
    try:
        subprocess.run([sys.executable, "src/carrega_metadados.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar gerenciamento de metadados")
    except FileNotFoundError:
        print("❌ Arquivo carrega_metadados.py não encontrado")

def executar_gera_sql():
    """Executa a geração de scripts SQL"""
    print("\n📄 GERAR SCRIPTS SQL (CREATE + INSERT)")
    print("-" * 40)
    print("Esta função converte planilhas em scripts SQL completos")
    print("Cria arquivos CREATE TABLE e INSERT prontos para execução")
    print()
    
    try:
        subprocess.run([sys.executable, "src/gera_create_inserts.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar geração de scripts SQL")
    except FileNotFoundError:
        print("❌ Arquivo gera_create_inserts.py não encontrado")

def mostrar_geoespaciais():
    """Mostra opções de dados geoespaciais"""
    print("\n🗺️  DADOS GEOESPACIAIS")
    print("-" * 40)
    print("Escolha uma opção:")
    print("1. Gerar Raster")
    print("2. Importar Raster Separado")
    print("3. Importar Raster Unido")
    print("0. Voltar ao menu principal")
    
    opcao = input("\nDigite sua escolha: ").strip()
    
    if opcao == "1":
        try:
            subprocess.run([sys.executable, "src/gerar_raster.py"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Erro ao executar gerar_raster.py")
    elif opcao == "2":
        try:
            subprocess.run([sys.executable, "src/importa_raster_separado.py"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Erro ao executar importa_raster_separado.py")
    elif opcao == "3":
        try:
            subprocess.run([sys.executable, "src/importa_raster_unidos.py"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Erro ao executar importa_raster_unidos.py")
    elif opcao == "0":
        return
    else:
        print("❌ Opção inválida")

def mostrar_ferramentas():
    """Mostra opções de ferramentas auxiliares"""
    print("\n🛠️  FERRAMENTAS AUXILIARES")
    print("-" * 40)
    print("Escolha uma opção:")
    print("1. Juntar Planilhas")
    print("2. Juntar Guias de Planilha")
    print("3. Transpor Planilha RH - Dados Superficiais")
    print("4. Transpor Planilha RH - Dados Subterrâneos")
    print("5. Executar Arquivo SQL")
    print("6. Exportar backup do banco de dados")
    print("0. Voltar ao menu principal")
    
    opcao = input("\nDigite sua escolha: ").strip()
    
    scripts = {
        "1": "tools/junta_planilhas.py",
        "2": "tools/junta_guias_planilha.py",
        "3": "tools/transpor_planilha_RH_dados_superficiais.py",
        "4": "tools/transpor_planilha_RH_dados_subteraneo.py",
        "5": "src/executa_arquivo_sql.py",
        "6": "src/exporta_backup_bd.py",
    }
    
    if opcao in scripts:
        try:
            subprocess.run([sys.executable, scripts[opcao]], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ Erro ao executar {scripts[opcao]}")
    elif opcao == "0":
        return
    else:
        print("❌ Opção inválida")

def mostrar_ajuda():
    """Mostra informações de ajuda"""
    print("\n❓ AJUDA")
    print("-" * 40)
    print("📖 Documentação completa: README.md")
    print("📋 Exemplos de uso: examples/exemplo_uso.md")
    print("⚙️  Template de configuração: examples/config_exemplo.env")
    print()
    print("🔧 Comandos diretos:")
    print("• poetry run python src/main.py")
    print("• poetry run python src/carrega_metadados.py")
    print("• poetry run python src/gera_create_inserts.py")
    print()
    print("📦 Scripts do Poetry:")
    print("• poetry run importa-planilha")
    print("• poetry run carrega-metadados")
    print("• poetry run gera-create-inserts")
    print()
    print("🐛 Problemas comuns:")
    print("• Verifique se o PostgreSQL está rodando")
    print("• Confirme as credenciais no arquivo .env")
    print("• Execute 'poetry install' se houver problemas de dependências")

def verificar_configuracao():
    """Verifica se a configuração está correta"""
    load_dotenv()
    
    print("🔍 Verificando configuração...")
    
    # Verificar variáveis de ambiente
    variaveis = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    faltando = []
    
    for var in variaveis:
        if not os.getenv(var):
            faltando.append(var)
    
    if faltando:
        print(f"⚠️  Variáveis de ambiente faltando: {', '.join(faltando)}")
        print("📝 Crie um arquivo .env baseado em examples/config_exemplo.env")
        return False
    else:
        print("✅ Configuração do banco de dados OK")
        return True

def main():
    """Função principal do sistema"""
    print("🚀 Iniciando Importador de Planilhas PostgreSQL...")
    
    # Verificar configuração
    if not verificar_configuracao():
        print("\n❌ Configure o arquivo .env antes de continuar")
        return
    
    while True:
        mostrar_menu()
        opcao = input("\nDigite sua escolha: ").strip()
        
        if opcao == "1":
            executar_metadados()
        elif opcao == "2":
            executar_gera_sql()
        elif opcao == "3":
            mostrar_geoespaciais()
        elif opcao == "4":
            mostrar_ferramentas()
        elif opcao == "5":
            mostrar_ajuda()
        elif opcao == "0":
            print("\n👋 Obrigado por usar o Importador de Planilhas PostgreSQL!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
        
        if opcao != "0":
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()