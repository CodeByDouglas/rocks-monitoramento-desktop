"""
Configurações de teste para o sistema de monitoramento Rocks
"""

import os
from config import *

# Sobrescrever configurações para testes
API_CONFIG.update({
    "base_url": "https://wretched-casket-7vrr9w7rv5q5fxjp5-8000.app.github.dev",  # Servidor de teste remoto
    "timeout": 2,  # Timeout muito baixo para testes
    "mock_responses": True,  # Usar respostas mock
})

LOGGING_CONFIG.update({
    "level": "DEBUG",  # Logging detalhado para testes
    "file": os.path.join("data", "rocks_monitoramento_test.log"),
})

# Configurações específicas de teste
TEST_CONFIG = {
    "auto_reload": False,
    "debug_mode": True,
    "test_mode": True,
    "mock_data": True,
    "fast_execution": True,
    "cleanup_after_test": True,
}

# Atualizar configurações principais
def get_test_config():
    """Retorna configurações de teste"""
    base_config = get_config()
    base_config["test"] = TEST_CONFIG
    return base_config

