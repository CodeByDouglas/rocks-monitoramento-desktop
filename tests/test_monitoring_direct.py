"""
Script para testar diretamente o endpoint de monitoramento
"""

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
        return "Teste-Direto"


def get_operating_system() -> str:
    try:
        system = platform.system()
        release = platform.release()
        return f"{system} {release}"
    except Exception:
        return "Linux"


def authenticate() -> str:
    """Realiza o login e retorna o token JWT."""
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

def test_monitoring_endpoint():
    """Testa o endpoint de monitoramento diretamente"""
    
    # URL do endpoint
    token = authenticate()

    # Coletar dados do sistema
    system_monitor = SystemMonitor()
    
    # Dados de exemplo (todos os status ativos)
    mac_address = get_mac_address()
    system_data = {
        "cpu": system_monitor.get_cpu_info(),
        "ram": system_monitor.get_ram_info(),
        "disco": system_monitor.get_disk_info(),
        "rede": system_monitor.get_network_info(),
        "temperatura": {"cpu": system_monitor.get_cpu_temperature()},
        "top_5_processos_cpu": system_monitor.get_top_processes(),
        "machine_info": {
            "hostname": get_username(),
            "mac_address": mac_address,
            "mac": mac_address,
            "operating_system": get_operating_system()
        },
        "timestamp": datetime.now().isoformat()
    }
    
    # Preparar payload
    payload = {
        "data": system_data
    }
    
    print("🚀 Testando endpoint de monitoramento...")
    print(f"📡 URL: {METRICS_URL}")
    print(f"📊 Dados a enviar:")
    print(f"   CPU: {system_data['cpu'].get('percentual_total', 'N/A')}%")
    print(f"   RAM: {system_data['ram'].get('percentual', 'N/A')}%")
    print(f"   Disco: {system_data['disco'].get('percentual', 'N/A')}%")
    print(f"   Rede: ↑{system_data['rede'].get('bytes_enviados_mb', 'N/A')}MB ↓{system_data['rede'].get('bytes_recebidos_mb', 'N/A')}MB")
    print(f"   Temperatura: {system_data['temperatura'].get('cpu', 'N/A')}°C")
    print(f"   Processos: {len(system_data['top_5_processos_cpu'])} processos")
    print("-" * 50)
    
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
        
        print(f"📤 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Sucesso! Endpoint funcionando corretamente.")
            try:
                response_data = response.json()
                print(f"📥 Resposta: {json.dumps(response_data, indent=2)}")
            except:
                print(f"📥 Resposta: {response.text}")
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"📥 Erro: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📥 Erro: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se o servidor está acessível.")
    except requests.exceptions.Timeout:
        print("❌ Timeout na conexão.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_monitoring_endpoint()
