"""
Módulo de API para comunicação com o servidor
Responsável por fazer requisições HTTP e gerenciar autenticação
"""

from .api_client import APIClient
from .auth_service import AuthService

__all__ = ['APIClient', 'AuthService']
