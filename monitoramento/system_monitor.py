"""
Monitor de sistema para coleta de dados da máquina
"""

import psutil
import json
import platform
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemMonitor:
    """Classe responsável por monitorar e coletar dados do sistema"""
    
    def __init__(self):
        self._last_network_counters = None
    
    def get_operating_system_info(self) -> Dict[str, Any]:
        """Obtém informações detalhadas do sistema operacional"""
        try:
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            os_info = {
                "sistema": system,
                "versao": release,
                "build": version,
                "arquitetura": machine,
                "processador": processor,
                "descricao_completa": f"{system} {release} ({machine})"
            }
            
            # Informações específicas por sistema operacional
            if system == "Windows":
                try:
                    win_ver = platform.win32_ver()
                    os_info.update({
                        "edicao": win_ver[0],
                        "build_number": win_ver[1],
                        "service_pack": win_ver[2]
                    })
                except:
                    pass
            elif system == "Linux":
                try:
                    distro = platform.linux_distribution()
                    os_info.update({
                        "distribuicao": distro[0],
                        "versao_distribuicao": distro[1],
                        "codinome": distro[2]
                    })
                except:
                    pass
            elif system == "Darwin":
                try:
                    mac_ver = platform.mac_ver()
                    os_info.update({
                        "versao_mac": mac_ver[0],
                        "build_mac": mac_ver[1]
                    })
                except:
                    pass
            
            return os_info
        except Exception as e:
            logger.error(f"Erro ao obter informações do SO: {e}")
            return {
                "sistema": "Unknown",
                "versao": "Unknown",
                "build": "Unknown",
                "arquitetura": "Unknown",
                "processador": "Unknown",
                "descricao_completa": "Unknown OS"
            }
    
    def get_cpu_info(self) -> Dict[str, Any]:
        """Obtém informações detalhadas sobre o CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            
            return {
                "percentual_total": round(cpu_percent, 1),
                "percentual_por_nucleo": [round(percent, 1) for percent in cpu_percent_per_core],
                "nucleos_fisicos": cpu_count_physical,
                "nucleos_logicos": cpu_count_logical
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações do CPU: {e}")
            return {
                "percentual_total": 0.0,
                "percentual_por_nucleo": [],
                "nucleos_fisicos": 0,
                "nucleos_logicos": 0
            }
    
    def get_ram_info(self) -> Dict[str, Any]:
        """Obtém informações sobre a memória RAM"""
        try:
            memory = psutil.virtual_memory()
            
            total_gb = round(memory.total / (1024**3), 1)
            available_gb = round(memory.available / (1024**3), 1)
            used_gb = round(memory.used / (1024**3), 1)
            percent = round(memory.percent, 1)
            
            return {
                "total_gb": total_gb,
                "disponivel_gb": available_gb,
                "usado_gb": used_gb,
                "percentual": percent
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações da RAM: {e}")
            return {
                "total_gb": 0.0,
                "disponivel_gb": 0.0,
                "usado_gb": 0.0,
                "percentual": 0.0
            }
    
    def get_disk_info(self, path: str = '/') -> Dict[str, Any]:
        """Obtém informações sobre o disco"""
        try:
            disk = psutil.disk_usage(path)
            
            total_gb = round(disk.total / (1024**3), 1)
            used_gb = round(disk.used / (1024**3), 1)
            free_gb = round(disk.free / (1024**3), 1)
            percent = round((disk.used / disk.total) * 100, 1)
            
            return {
                "total_gb": total_gb,
                "usado_gb": used_gb,
                "livre_gb": free_gb,
                "percentual": percent
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações do disco: {e}")
            return {
                "total_gb": 0.0,
                "usado_gb": 0.0,
                "livre_gb": 0.0,
                "percentual": 0.0
            }
    
    def get_network_info(self) -> Dict[str, Any]:
        """Obtém informações sobre o tráfego de rede"""
        try:
            network = psutil.net_io_counters()
            
            bytes_sent_mb = round(network.bytes_sent / (1024**2), 2)
            bytes_recv_mb = round(network.bytes_recv / (1024**2), 2)
            
            return {
                "bytes_enviados_mb": bytes_sent_mb,
                "bytes_recebidos_mb": bytes_recv_mb
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações da rede: {e}")
            return {
                "bytes_enviados_mb": 0.0,
                "bytes_recebidos_mb": 0.0
            }
    
    def get_cpu_temperature(self) -> float:
        """Obtém a temperatura do CPU"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        return round(entries[0].current, 1)
        except Exception as e:
            logger.warning(f"Não foi possível obter temperatura do CPU: {e}")
        
        # Valor padrão se não conseguir obter a temperatura
        return 58.0
    
    def get_top_processes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtém os processos que mais consomem CPU"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 0:
                        processes.append({
                            "nome": proc_info['name'],
                            "cpu_percent": round(proc_info['cpu_percent'], 1),
                            "memoria_mb": round(proc_info['memory_info'].rss / (1024**2), 1)
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Ordena por uso de CPU e pega os top N
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:limit]
        except Exception as e:
            logger.error(f"Erro ao obter processos: {e}")
            return []
    
    def collect_system_data(self) -> Dict[str, Any]:
        """Coleta todos os dados do sistema"""
        try:
            dados = {
                "timestamp": datetime.now().isoformat(),
                "sistema_operacional": self.get_operating_system_info(),
                "cpu": self.get_cpu_info(),
                "ram": self.get_ram_info(),
                "disco": self.get_disk_info(),
                "rede": self.get_network_info(),
                "temperatura": {
                    "cpu": self.get_cpu_temperature()
                },
                "top_5_processos_cpu": self.get_top_processes(5)
            }
            
            return dados
        except Exception as e:
            logger.error(f"Erro ao coletar dados do sistema: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def save_data_to_json(self, data: Dict[str, Any], filename: str = None) -> bool:
        """Salva os dados em formato JSON"""
        try:
            if filename is None:
                # Usar caminho das configurações centralizadas
                from config import FILE_CONFIG
                filename = FILE_CONFIG["system_data_file"]
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Dados salvos em {filename}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")
            return False
    
    def get_machine_info(self) -> Dict[str, str]:
        """Obtém informações básicas da máquina"""
        try:
            import socket
            import uuid
            
            return {
                "hostname": socket.gethostname(),
                "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                                       for elements in range(0,2*6,2)][::-1]),
                "operating_system": self.get_operating_system_info()["descricao_completa"]
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações da máquina: {e}")
            return {
                "hostname": "unknown",
                "mac_address": "unknown",
                "operating_system": "unknown"
            }


# Função de conveniência para uso direto
def monitor_system() -> Dict[str, Any]:
    """Função de conveniência para monitorar o sistema"""
    monitor = SystemMonitor()
    return monitor.collect_system_data()


if __name__ == "__main__":
    # Teste do monitor
    monitor = SystemMonitor()
    data = monitor.collect_system_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
