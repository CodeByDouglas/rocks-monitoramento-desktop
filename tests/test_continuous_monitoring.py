"""
Script para testar o monitoramento contínuo diretamente
"""

import time
import requests
import json
from datetime import datetime
from monitoramento.system_monitor import SystemMonitor

def test_continuous_monitoring():
    """Testa o monitoramento contínuo"""
    
    # URL do endpoint
    url = "https://super-trout-4jgg76qgjvpxcq655-8000.app.github.dev/api/maquina/status"
    
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
    print(f"📡 URL: {url}")
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
                "hostname": "Teste-Continuo",
                "mac_address": "50-A1-32-1E-44-FC",
                "operating_system": "Windows 11 (11)"
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
                    url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "Rocks-Monitoramento-Desktop/1.0"
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
