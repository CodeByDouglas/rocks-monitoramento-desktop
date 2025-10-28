"""
Script para testar o monitoramento contínuo diretamente
"""

import time
import requests
import json
import socket
import platform
import uuid
from datetime import datetime
from monitoramento.system_monitor import SystemMonitor

LOGIN_URL = "https://wretched-casket-7vrr9w7rv5q5fxjp5-8000.app.github.dev/api/login"
METRICS_URL = "https://wretched-casket-7vrr9w7rv5q5fxjp5-8000.app.github.dev/api/maquina/status"
EMAIL = "developer@rocks.com"
PASSWORD = "Dev@Rocks2025"


def get_mac_address() -> str:
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                       for elements in range(0, 2 * 6, 2)][::-1])
        return mac.upper()
    except Exception:
        return "00:00:00:00:00:00"


def get_username() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "Teste-Continuo"


def get_operating_system() -> str:
    try:
        system = platform.system()
        release = platform.release()
        return f"{system} {release}"
    except Exception:
        return "Linux"


def authenticate() -> str:
    payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "mac_address": get_mac_address(),
        "username": get_username(),
        "c": get_operating_system(),
    }

    response = requests.post(
        LOGIN_URL,
        json=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Rocks-Monitoramento-Desktop/1.0"},
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()
    return data.get("token", "")

def test_continuous_monitoring():
    """Testa o monitoramento contínuo"""
    
    # URL do endpoint
    token = authenticate()

    # Configuração de monitoramento
    frequency = 5  # segundos
    monitored_status = {
        "cpu": True,
        "ram": True,
        "disco": True,
        "rede": True,
        "temperatura": True,
        "processos": True
    }
    
    # Coletar dados do sistema
    system_monitor = SystemMonitor()
    
    print("🚀 Iniciando monitoramento contínuo...")
    print(f"📡 URL: {METRICS_URL}")
    print(f"⏱️ Frequência: {frequency} segundos")
    print(f"📊 Status monitorados: {list(monitored_status.keys())}")
    print("=" * 60)
    
    cycle = 1
    try:
        while True:
            print(f"\n🔄 Ciclo {cycle} - {datetime.now().strftime('%H:%M:%S')}")
            
            # Coletar dados do sistema baseado nos status monitorados
            system_data = {}
            
            if monitored_status.get("cpu", False):
                system_data["cpu"] = system_monitor.get_cpu_info()
            
            if monitored_status.get("ram", False):
                system_data["ram"] = system_monitor.get_ram_info()
            
            if monitored_status.get("disco", False):
                system_data["disco"] = system_monitor.get_disk_info()
            
            if monitored_status.get("rede", False):
                system_data["rede"] = system_monitor.get_network_info()
            
            if monitored_status.get("temperatura", False):
                system_data["temperatura"] = {"cpu": system_monitor.get_cpu_temperature()}
            
            if monitored_status.get("processos", False):
                system_data["top_5_processos_cpu"] = system_monitor.get_top_processes()
            
            # Adicionar informações da máquina
            system_data["machine_info"] = {
                "hostname": get_username(),
                "mac_address": get_mac_address(),
                "mac": get_mac_address(),
                "operating_system": get_operating_system()
            }
            system_data["timestamp"] = datetime.now().isoformat()
            
            # Preparar payload
            payload = {
                "data": system_data
            }
            
            # Mostrar dados coletados
            print(f"📊 Dados coletados:")
            if "cpu" in system_data:
                print(f"   CPU: {system_data['cpu'].get('percentual_total', 'N/A')}%")
            if "ram" in system_data:
                print(f"   RAM: {system_data['ram'].get('percentual', 'N/A')}%")
            if "disco" in system_data:
                print(f"   Disco: {system_data['disco'].get('percentual', 'N/A')}%")
            if "rede" in system_data:
                print(f"   Rede: ↑{system_data['rede'].get('bytes_enviados_mb', 'N/A')}MB ↓{system_data['rede'].get('bytes_recebidos_mb', 'N/A')}MB")
            if "temperatura" in system_data:
                print(f"   Temperatura: {system_data['temperatura'].get('cpu', 'N/A')}°C")
            if "top_5_processos_cpu" in system_data:
                print(f"   Processos: {len(system_data['top_5_processos_cpu'])} processos")
            
            try:
                # Fazer requisição PUT
                response = requests.put(
                    METRICS_URL,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "Rocks-Monitoramento-Desktop/1.0",
                        "Authorization": f"Bearer {token}",
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    print("✅ Dados enviados com sucesso!")
                else:
                    print(f"❌ Erro HTTP {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("❌ Erro de conexão")
            except requests.exceptions.Timeout:
                print("❌ Timeout na conexão")
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
            
            print(f"⏳ Aguardando {frequency} segundos...")
            time.sleep(frequency)
            cycle += 1
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento interrompido pelo usuário")
        print(f"📈 Total de ciclos executados: {cycle-1}")

if __name__ == "__main__":
    test_continuous_monitoring()
