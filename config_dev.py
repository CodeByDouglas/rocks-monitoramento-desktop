"""
Configurações de desenvolvimento para o sistema de monitoramento Rocks
"""

import os
from config import *

# Sobrescrever configurações para desenvolvimento
API_CONFIG.update({
    "base_url": "http://localhost:8000",  # Servidor local para desenvolvimento
    "timeout": 5,  # Timeout menor para desenvolvimento
})

LOGGING_CONFIG.update({
    "level": "DEBUG",  # Logging mais detalhado para desenvolvimento
})

# Configurações específicas de desenvolvimento
DEV_CONFIG = {
    "auto_reload": True,
    "debug_mode": True,
    "test_server_port": 8000,
    "mock_api": False,  # Usar API real ou mock
}

# Atualizar configurações principais
def get_dev_config():
    """Retorna configurações de desenvolvimento"""
    base_config = get_config()
    base_config["dev"] = DEV_CONFIG
    return base_config

