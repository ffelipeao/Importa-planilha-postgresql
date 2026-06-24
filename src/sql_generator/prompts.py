"""Prompts interativos para geração de SQL."""

from sql_generator.encoding import resolver_codificacao


def perguntar_codificacao() -> str:
    """Solicita ao usuário a codificação para leitura de arquivos CSV."""
    print("\nCodificação para leitura de arquivos CSV:")
    print("  1 - UTF-8 (padrão)")
    print("  2 - ISO-8859-1 (Latin-1)")
    print("  3 - Windows-1252")
    print("  ou informe outro nome de codificação suportado pelo Python")
    codific = input("Informe a opção (Enter para UTF-8): ").strip()
    if not codific:
        codific = '1'
    codificacao = resolver_codificacao(codific)
    print(f'Codificação selecionada: {codificacao}')
    return codificacao


def perguntar_modo_tipos() -> bool:
    """Solicita ao usuário o modo de definição dos tipos de colunas no CREATE TABLE."""
    print("\nModo de tipos de dados para CREATE TABLE:")
    print("  1 - Todos os campos como text (padrão)")
    print("  2 - Inferir tipos automaticamente")
    opcao = input("Informe a opção (Enter para text): ").strip()
    inferir = opcao == '2'
    modo = 'inferência automática' if inferir else 'text'
    print(f'Modo selecionado: {modo}')
    return inferir


def perguntar_validacao_completa() -> bool:
    """Solicita se a inferência deve validar todas as colunas em todas as linhas."""
    print("\nValidação de tipos inferidos:")
    print("  1 - Rápida: amostra na memória + ajuste de VARCHAR (padrão, mais rápida)")
    print("  2 - Completa: uma passagem por todas as colunas e linhas (mais segura)")
    opcao = input("Informe a opção (Enter para rápida): ").strip()
    completa = opcao == '2'
    modo = 'validação completa' if completa else 'validação rápida'
    print(f'Validação selecionada: {modo}')
    return completa


def perguntar_schema(padrao: str = 'dados_gts') -> str:
    """Solicita ao usuário o schema PostgreSQL de destino."""
    print("\nSchema PostgreSQL para gerar o SQL:")
    nome = input(f"Informe o nome do schema (Enter para {padrao}): ").strip()
    if not nome:
        nome = padrao
    print(f'Schema selecionado: {nome}')
    return nome
