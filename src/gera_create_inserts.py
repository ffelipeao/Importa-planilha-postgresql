"""
Gera scripts SQL (CREATE TABLE + INSERT) a partir de planilhas Excel ou CSV.

Este módulo mantém compatibilidade com imports e execução direta existentes,
delegando a implementação ao pacote sql_generator.
"""

from sql_generator.cli import main
from sql_generator.column_normalizer import normalizar_colunas, normalizar_nome_coluna
from sql_generator.constants import (
    AMOSTRA_ALEATORIA,
    AMOSTRA_FIM,
    AMOSTRA_INICIO,
    AMOSTRA_MEIO,
    INT32_MAX,
    INT32_MIN,
    LIMITE_CARACTERES_TEXTO,
    MAX_LINHAS_AMOSTRA,
    PADROES_DATA,
    PADROES_TIMESTAMP,
    VALORES_BOOLEANOS,
    VARCHAR_MARGEM_SEGURANCA,
    VARCHAR_TAMANHO_MINIMO,
)
from sql_generator.create_table_generator import gerar_create_table
from sql_generator.encoding import detectar_codificacao, resolver_codificacao
from sql_generator.enums import CategoriaValor
from sql_generator.insert_generator import formatar_valor_insert, gerar_insert_sql
from sql_generator.models import EstadoInferenciaColuna
from sql_generator.orchestrator import escrever_arquivo_sql, gerar_sql
from sql_generator.prompts import (
    perguntar_codificacao,
    perguntar_modo_tipos,
    perguntar_schema,
    perguntar_validacao_completa,
)
from sql_generator.sampling import selecionar_indices_amostra
from sql_generator.spreadsheet_reader import (
    contar_linhas_csv,
    contar_linhas_excel,
    extrair_amostra_do_dataframe,
    ler_amostra_para_inferencia,
    ler_arquivo,
    ler_cabecalho_csv,
    ler_cabecalho_excel,
    ler_linhas_csv_por_indices,
    ler_linhas_excel_por_indices,
)
from sql_generator.type_inferencer import (
    ajustar_tipos_pelo_dataset_completo,
    arredondar_tamanho_varchar,
    calcular_tipo_cadeia_por_tamanho,
    coluna_exige_integer_por_nome,
    combinar_categorias,
    finalizar_tipo_coluna,
    inferir_tipo_coluna,
    inferir_tipo_coluna_completo,
    inferir_tipos_colunas,
    inferir_varchar,
    tipo_eh_cadeia_curta,
    tipo_inteiro_por_magnitude,
    validar_tipos_pelo_dataset_completo,
)
from sql_generator.value_classifier import classificar_valor
from sql_generator.value_patterns import (
    corresponde_booleano,
    corresponde_data,
    corresponde_decimal,
    corresponde_inteiro,
    corresponde_timestamp,
)
from sql_generator.value_utils import (
    citar_identificador,
    coluna_excede_limite_texto,
    format_file_name,
    sanitizar_identificador,
    tamanho_maximo_amostra,
    tratar_dado,
    valor_para_texto,
    valor_vazio,
    valores_contem_texto_nao_numerico,
    valores_excedem_limite_texto,
)

__all__ = [
    'AMOSTRA_ALEATORIA',
    'AMOSTRA_FIM',
    'AMOSTRA_INICIO',
    'AMOSTRA_MEIO',
    'CategoriaValor',
    'EstadoInferenciaColuna',
    'INT32_MAX',
    'INT32_MIN',
    'LIMITE_CARACTERES_TEXTO',
    'MAX_LINHAS_AMOSTRA',
    'PADROES_DATA',
    'PADROES_TIMESTAMP',
    'VALORES_BOOLEANOS',
    'VARCHAR_MARGEM_SEGURANCA',
    'VARCHAR_TAMANHO_MINIMO',
    'ajustar_tipos_pelo_dataset_completo',
    'arredondar_tamanho_varchar',
    'calcular_tipo_cadeia_por_tamanho',
    'citar_identificador',
    'classificar_valor',
    'coluna_excede_limite_texto',
    'coluna_exige_integer_por_nome',
    'combinar_categorias',
    'contar_linhas_csv',
    'contar_linhas_excel',
    'corresponde_booleano',
    'corresponde_data',
    'corresponde_decimal',
    'corresponde_inteiro',
    'corresponde_timestamp',
    'detectar_codificacao',
    'escrever_arquivo_sql',
    'extrair_amostra_do_dataframe',
    'finalizar_tipo_coluna',
    'format_file_name',
    'formatar_valor_insert',
    'gerar_create_table',
    'gerar_insert_sql',
    'gerar_sql',
    'inferir_tipo_coluna',
    'inferir_tipo_coluna_completo',
    'inferir_tipos_colunas',
    'inferir_varchar',
    'ler_amostra_para_inferencia',
    'ler_arquivo',
    'ler_cabecalho_csv',
    'ler_cabecalho_excel',
    'ler_linhas_csv_por_indices',
    'ler_linhas_excel_por_indices',
    'main',
    'normalizar_colunas',
    'normalizar_nome_coluna',
    'perguntar_codificacao',
    'perguntar_modo_tipos',
    'perguntar_schema',
    'perguntar_validacao_completa',
    'resolver_codificacao',
    'sanitizar_identificador',
    'selecionar_indices_amostra',
    'tamanho_maximo_amostra',
    'tipo_eh_cadeia_curta',
    'tipo_inteiro_por_magnitude',
    'tratar_dado',
    'validar_tipos_pelo_dataset_completo',
    'valor_para_texto',
    'valor_vazio',
    'valores_contem_texto_nao_numerico',
    'valores_excedem_limite_texto',
]

if __name__ == "__main__":
    main()
