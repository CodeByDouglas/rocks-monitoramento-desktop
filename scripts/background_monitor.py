#!/usr/bin/env python3
"""
Script para monitoramento contínuo em segundo plano
Este script pode ser executado independentemente da interface gráfica
"""

import json
import time
import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FILE_CONFIG, LOGGING_CONFIG
from api.auth_service import AuthService
from monitoramento.system_monitor import SystemMonitor

# Configurar logging usando as configurações centralizadas
log_file = FILE_CONFIG["machine_config_file"].replace("configuracao_maquina.json", "background_monitor.log")
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BackgroundMonitor:
    """Monitoramento contínuo em segundo plano"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.frequency = config.get("update_frequency", 5)
        self.monitored_status = config.get("monitored_status", {})
        self.is_running = False
        
        # Inicializar serviços
        self.auth_service = AuthService()
        self.system_monitor = SystemMonitor()
        self.api_client = self.auth_service.api_client
        
        logger.info(f"Background monitor inicializado - Frequência: {self.frequency}s")
    
    def start(self):
        """Inicia o monitoramento contínuo"""
        self.is_running = True
        logger.info("Iniciando monitoramento contínuo em segundo plano")
        
        try:
            while self.is_running:
                # Aguardar o tempo definido na frequência
                time.sleep(self.frequency)
                
                if not self.is_running:
                    break
                
                # Coletar dados do sistema
                system_data = self.collect_system_data()
                
                # Enviar dados para a API
                self.send_system_data(system_data)
                
        except KeyboardInterrupt:
            logger.info("Monitoramento interrompido pelo usuário")
        except Exception as e:
            logger.error(f"Erro no monitoramento: {e}")
        finally:
            self.is_running = False
            logger.info("Monitoramento finalizado")
    
    def stop(self):
        """Para o monitoramento"""
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
            
            # Informações da máquina
            mac_address = self.auth_service.get_mac_address()
            data["machine_info"] = {
                "hostname": self.auth_service.get_hostname(),
                "mac_address": mac_address,
                "mac": mac_address,
                "operating_system": self.auth_service.get_operating_system(),
                "type": self.auth_service.get_machine_type()
            }
            
            # Timestamp
            data["timestamp"] = datetime.now().isoformat()
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados do sistema: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def send_system_data(self, system_data: Dict[str, Any]):
        """Envia dados do sistema para a API"""
        try:
            # Preparar payload
            payload = {
                "data": system_data
            }
            
            # Enviar para a API
            token = self.auth_service.get_auth_token()
            if not token:
                logger.error("Monitor não autenticado. Não é possível enviar dados.")
                return

            response = self.api_client.update_machine_status(
                payload,
                auth_token=token
            )
            
            if response.success:
                logger.info("Dados enviados com sucesso para a API")
            else:
                logger.error(f"Erro ao enviar dados: {response.error}")
                
        except Exception as e:
            logger.error(f"Erro ao enviar dados para a API: {e}")

def load_config_from_file() -> Dict[str, Any]:
    """Carrega configuração do arquivo JSON"""
    try:
        config_file = FILE_CONFIG["machine_config_file"]
        
        if not os.path.exists(config_file):
            logger.error(f"Arquivo de configuração não encontrado: {config_file}")
            return {}
        
        with open(config_file, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        
        # Extrair configuração da estrutura do arquivo
        if "configuration" in config_data:
            config = config_data["configuration"]
            config["monitored_status"] = config.get("monitored_status", {})
            config["update_frequency"] = config.get("update_frequency", 5)
            return config
        else:
            logger.error("Estrutura de configuração inválida")
            return {}
            
    except Exception as e:
        logger.error(f"Erro ao carregar configuração: {e}")
        return {}

def main():
    """Função principal"""
    try:
        # Carregar configuração
        config = load_config_from_file()
        
        if not config:
            logger.error("Não foi possível carregar a configuração")
            return
        
        # Criar e iniciar monitor
        monitor = BackgroundMonitor(config)
        monitor.start()
        
    except KeyboardInterrupt:
        logger.info("Script interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro no script principal: {e}")

if __name__ == "__main__":
    main()
