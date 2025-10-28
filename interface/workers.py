"""
Workers para operações assíncronas da interface
"""

import logging
from typing import Dict, Any
from datetime import datetime
from PySide6.QtCore import QThread, Signal
from api.auth_service import AuthService

logger = logging.getLogger(__name__)


class LoginWorker(QThread):
    """Thread para fazer a requisição HTTP de login"""
    login_success = Signal(dict)  # Sinal para sucesso com dados da máquina
    login_error = Signal(str)     # Sinal para erro de autenticação
    network_error = Signal(str)   # Sinal para erro de rede
    
    def __init__(self, email: str, password: str):
        super().__init__()
        self.email = email
        self.password = password
        # Usar a instância global do AuthService
        from .utils import get_auth_service
        self.auth_service = get_auth_service()
        
    def run(self):
        """Executa a autenticação em thread separada"""
        try:
            logger.info(f"Tentando login - Email: {self.email}")
            
            # Fazer a autenticação
            response = self.auth_service.authenticate(self.email, self.password)
            
            if response.success:
                logger.info("Login bem-sucedido!")
                self.login_success.emit(response.data or {})
            else:
                logger.error(f"Erro no login: {response.error}")
                self.login_error.emit(response.error or "Erro desconhecido")
                
        except Exception as e:
            logger.error(f"Erro inesperado no login: {e}")
            self.network_error.emit(f"Erro inesperado: {str(e)}")


class SystemMonitoringWorker(QThread):
    """Thread para monitoramento contínuo do sistema em segundo plano"""
    monitoring_started = Signal()
    monitoring_stopped = Signal()
    monitoring_error = Signal(str)
    data_sent = Signal()
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.is_running = False
        self.frequency = config.get("update_frequency", 5)
        self.monitored_status = config.get("monitored_status", {})
        
        # Usar a instância global do AuthService
        from .utils import get_auth_service
        self.auth_service = get_auth_service()
        
        # Importar o monitor do sistema
        from monitoramento.system_monitor import SystemMonitor
        self.system_monitor = SystemMonitor()
        
    def run(self):
        """Executa o monitoramento contínuo em thread separada"""
        self.is_running = True
        self.monitoring_started.emit()
        
        logger.info(f"Iniciando monitoramento contínuo - Frequência: {self.frequency}s")
        
        try:
            while self.is_running:
                # Aguardar o tempo definido na frequência
                self.msleep(self.frequency * 1000)  # Converter para milissegundos
                
                if not self.is_running:
                    break
                
                # Coletar dados do sistema baseado nos status monitorados
                system_data = self.collect_system_data()
                
                # Enviar dados para a API
                self.send_system_data(system_data)
                
        except Exception as e:
            logger.error(f"Erro no monitoramento contínuo: {e}")
            self.monitoring_error.emit(f"Erro no monitoramento: {str(e)}")
        finally:
            self.is_running = False
            self.monitoring_stopped.emit()
            logger.info("Monitoramento contínuo finalizado")
    
    def stop_monitoring(self):
        """Para o monitoramento contínuo"""
        self.is_running = False
        logger.info("Solicitação para parar monitoramento")
    
    def collect_system_data(self) -> Dict[str, Any]:
        """Coleta dados do sistema baseado nos status monitorados"""
        try:
            data = {}
            
            # CPU
            if self.monitored_status.get("cpu", False):
                data["cpu"] = self.system_monitor.get_cpu_info()
            
            # RAM
            if self.monitored_status.get("ram", False):
                data["ram"] = self.system_monitor.get_ram_info()
            
            # Disco
            if self.monitored_status.get("disco", False):
                data["disco"] = self.system_monitor.get_disk_info()
            
            # Rede
            if self.monitored_status.get("rede", False):
                data["rede"] = self.system_monitor.get_network_info()
            
            # Temperatura
            if self.monitored_status.get("temperatura", False):
                data["temperatura"] = {"cpu": self.system_monitor.get_cpu_temperature()}
            
            # Processos
            if self.monitored_status.get("processos", False):
                data["top_5_processos_cpu"] = self.system_monitor.get_top_processes()
            
            # Adicionar informações da máquina
            data["machine_info"] = self.auth_service.get_machine_info()
            data["timestamp"] = datetime.now().isoformat()
            
            logger.debug(f"Dados coletados: {len(data)} categorias")
            return data
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados do sistema: {e}")
            raise
    
    def send_system_data(self, system_data: Dict[str, Any]):
        """Envia dados do sistema para a API"""
        try:
            from api.api_client import APIClient
            
            # Preparar payload
            payload = {
                "data": system_data
            }
            
            # Enviar via PUT para /api/maquina/status
            api_client = APIClient()
            response = api_client.update_machine_status(payload)
            
            if response.success:
                logger.debug("Dados do sistema enviados com sucesso")
                self.data_sent.emit()
            else:
                logger.warning(f"Erro ao enviar dados: {response.error}")
                
        except Exception as e:
            logger.error(f"Erro ao enviar dados do sistema: {e}")
            # Não interromper o loop por erro de envio


class SystemDataWorker(QThread):
    """Thread para enviar dados do sistema para a API"""
    send_success = Signal()
    send_error = Signal(str)
    
    def __init__(self, system_data: Dict[str, Any], auth_service: AuthService):
        super().__init__()
        self.system_data = system_data
        self.auth_service = auth_service
        
    def run(self):
        """Executa o envio de dados em thread separada"""
        try:
            logger.info("Enviando dados do sistema para a API")
            
            response = self.auth_service.send_system_data(self.system_data)
            
            if response.success:
                logger.info("Dados enviados com sucesso")
                self.send_success.emit()
            else:
                logger.error(f"Erro ao enviar dados: {response.error}")
                self.send_error.emit(response.error or "Erro desconhecido")
                
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar dados: {e}")
            self.send_error.emit(f"Erro inesperado: {str(e)}")


class ConfigUpdateWorker(QThread):
    """Thread para enviar configuração da máquina para a API"""
    update_success = Signal()
    update_error = Signal(str)
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        # Usar a instância global do AuthService
        from .utils import get_auth_service
        self.auth_service = get_auth_service()
        
    def run(self):
        """Executa o envio da configuração em thread separada"""
        try:
            logger.info("Enviando configuração da máquina para a API")
            
            response = self.auth_service.update_machine_configuration(self.config)
            
            if response.success:
                logger.info("Configuração enviada com sucesso")
                
                # Salvar configurações em arquivo JSON
                self.save_config_to_file()
                
                self.update_success.emit()
            else:
                logger.error(f"Erro ao enviar configuração: {response.error}")
                self.update_error.emit(response.error or "Erro desconhecido")
                
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar configuração: {e}")
            self.update_error.emit(f"Erro inesperado: {str(e)}")
    
    def save_config_to_file(self):
        """Salva as configurações em arquivo JSON"""
        try:
            import json
            import os
            
            # Obter informações da máquina
            machine_info = self.auth_service.get_machine_info()
            
            # Preparar dados para salvar
            config_data = {
                "timestamp": datetime.now().isoformat(),
                "machine_info": {
                    "hostname": machine_info["hostname"],
                    "mac_address": machine_info["mac_address"],
                    "operating_system": machine_info["operating_system"],
                    "type": self.auth_service.get_machine_type()
                },
                "configuration": {
                    "machine_name": self.config.get("machine_name", ""),
                    "monitored_status": self.config.get("monitored_status", {}),
                    "update_frequency": self.config.get("update_frequency", 1),
                    "notifications": self.config.get("notifications", False),
                    "start_with_os": self.config.get("start_with_os", False)
                }
            }
            
            # Usar caminho das configurações centralizadas
            from config import FILE_CONFIG
            filename = FILE_CONFIG["machine_config_file"]
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Salvar arquivo (sobrescreve se já existir)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuração salva/atualizada em arquivo: {filename}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar configuração em arquivo: {e}")
            # Não falhar o processo se não conseguir salvar o arquivo
