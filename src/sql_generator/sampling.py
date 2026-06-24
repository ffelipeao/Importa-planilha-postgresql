"""Seleção de amostras para inferência de tipos."""

import random
from typing import List, Set

from sql_generator.constants import (
    AMOSTRA_ALEATORIA,
    AMOSTRA_FIM,
    AMOSTRA_INICIO,
    AMOSTRA_MEIO,
    MAX_LINHAS_AMOSTRA,
)


def selecionar_indices_amostra(total_linhas: int, max_linhas: int = MAX_LINHAS_AMOSTRA) -> List[int]:
    if total_linhas <= 0:
        return []
    if total_linhas <= max_linhas:
        return list(range(total_linhas))

    indices: Set[int] = set()

    indices.update(range(min(AMOSTRA_INICIO, total_linhas)))

    inicio_meio = max(0, (total_linhas // 2) - (AMOSTRA_MEIO // 2))
    indices.update(range(inicio_meio, min(inicio_meio + AMOSTRA_MEIO, total_linhas)))

    indices.update(range(max(0, total_linhas - AMOSTRA_FIM), total_linhas))

    restante = sorted(set(range(total_linhas)) - indices)
    if restante:
        quantidade_aleatoria = min(AMOSTRA_ALEATORIA, len(restante))
        indices.update(random.sample(restante, quantidade_aleatoria))

    return sorted(indices)
