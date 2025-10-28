"""
Configurações de produção para o sistema de monitoramento Rocks
"""

import os
from config import *

# Sobrescrever configurações para produção
API_CONFIG.update({
    "base_url": os.getenv("ROCKS_API_URL", "https://api.rocks.com"),  # URL de produção
    "timeout": 15,  # Timeout maior para produção
    "retry_attempts": 3,  # Tentativas de retry
})

LOGGING_CONFIG.update({
    "level": "WARNING",  # Logging menos verboso para produção
    "file": os.path.join("data", "rocks_monitoramento_prod.log"),
})

# Configurações específicas de produção
PROD_CONFIG = {
    "auto_reload": False,
    "debug_mode": False,
    "performance_monitoring": True,
    "error_reporting": True,
    "backup_config": True,
}

# Atualizar configurações principais
def get_prod_config():
    """Retorna configurações de produção"""
    base_config = get_config()
    base_config["prod"] = PROD_CONFIG
    return base_config

