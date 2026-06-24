"""Constantes usadas na geração de SQL e inferência de tipos."""

import re

MAX_LINHAS_AMOSTRA = 200
AMOSTRA_INICIO = 50
AMOSTRA_MEIO = 50
AMOSTRA_FIM = 50
AMOSTRA_ALEATORIA = 50
LIMITE_CARACTERES_TEXTO = 50
VARCHAR_TAMANHO_MINIMO = 1
VARCHAR_MARGEM_SEGURANCA = 2
INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647

VALORES_BOOLEANOS = {
    'true', 'false', 't', 'f', 'sim', 'nao', 'não', 'yes', 'no', 'y', 'n', '1', '0',
}

PADROES_DATA = (
    re.compile(r'^\d{4}-\d{2}-\d{2}$'),
    re.compile(r'^\d{2}/\d{2}/\d{4}$'),
    re.compile(r'^\d{2}-\d{2}-\d{4}$'),
    re.compile(r'^\d{4}/\d{2}/\d{2}$'),
)

PADROES_TIMESTAMP = (
    re.compile(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?$'),
    re.compile(r'^\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}$'),
    re.compile(r'^\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}$'),
    re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$'),
)
