"""
Utilitários da interface
"""

import os
from typing import Optional
from api.auth_service import AuthService

# Instância global do serviço de autenticação
_auth_service: Optional[AuthService] = None


def get_auth_service() -> AuthService:
    """Retorna a instância global do serviço de autenticação"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service


def get_logo_path() -> str:
    """Obtém o caminho para a logo da Rocks"""
    return os.path.join(os.path.dirname(__file__), "image", "logo_rocks.png")


def logo_exists() -> bool:
    """Verifica se a logo existe"""
    return os.path.exists(get_logo_path())


def get_mac_address() -> str:
    """Obtém o endereço MAC da máquina"""
    return get_auth_service().get_mac_address()


def get_username() -> str:
    """Obtém o nome do usuário da máquina"""
    return get_auth_service().get_hostname()


def get_machine_icon_path() -> str:
    """Obtém o caminho do ícone baseado no tipo de máquina"""
    machine_type = get_auth_service().get_machine_type()
    
    if machine_type.lower() == "server":
        return os.path.join(os.path.dirname(__file__), "image", "icone_server.png")
    else:
        # Padrão para PC ou qualquer outro tipo
        return os.path.join(os.path.dirname(__file__), "image", "icone_pc.png")


def machine_icon_exists() -> bool:
    """Verifica se o ícone da máquina existe"""
    return os.path.exists(get_machine_icon_path())
