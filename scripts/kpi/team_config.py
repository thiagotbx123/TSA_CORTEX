"""Shared KPI team member configuration.

Single source of truth for person name → TSA code mappings and Linear user IDs.
Import from here in merge_opossum_data.py and refresh_linear_cache.py.
"""

# Full name → TSA code (used when matching by assignee display name)
PERSON_MAP = {
    'Thaís Linzmaier': 'THAIS',
    'Yasmim Arsego': 'YASMIM',
    'Thiago Rodrigues': 'THIAGO',
    'Carlos Guilherme Matos de Almeida da Silva': 'CARLOS',
    'Alexandra Lacerda': 'ALEXANDRA',
    'Diego Cavalli': 'DIEGO',
    'Gabrielle Cupello': 'GABI',
}

# Linear user ID → TSA code (used when matching by assigneeId)
PERSON_MAP_BY_ID = {
    'a6063009-d822-49f1-a638-6cebfe59e89e': 'THIAGO',
    'b13ca864-e0f4-4ff6-b020-ec3f4491643e': 'CARLOS',
    '19b6975e-3026-450b-bc01-f468ad543028': 'ALEXANDRA',
    '717e7b13-d840-41c0-baeb-444354c8ff91': 'DIEGO',
    'd9745bdb-7138-4345-9303-516aa6e4ec39': 'GABI',
    '0879df15-56d6-477f-944d-df033121641a': 'THAIS',
    'df4a6bcf-c519-469d-bb40-b1a0e93d0041': 'YASMIM',
}

# KPI_MEMBERS mirrors PERSON_MAP_BY_ID — used by refresh_linear_cache.py for fetch loops
KPI_MEMBERS = PERSON_MAP_BY_ID
