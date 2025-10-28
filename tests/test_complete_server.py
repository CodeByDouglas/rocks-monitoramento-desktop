"""
Servidor de teste completo para simular todos os endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Armazenar dados recebidos
received_data = []

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint de login"""
    try:
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
        
        print(f"🔐 Login tentativa: {email}")
        
        # Simular autenticação
        if email == "teste@rocks.com" and password == "123456":
            response_data = {
                "success": True,
                "message": "Login realizado com sucesso",
                "data": {
                    "Nome": "Máquina Teste",
                    "Notificar": True,
                    "Frequency": 5,
                    "iniciarSO": True,
                    "status": {
                        "CPU": False,
                        "DISCO": True,
                        "PROCESSO": True,
                        "RAM": True,
                        "REDE": False,
                        "TEMPERATURA": False,
                        "type": "server"
                    }
                }
            }
            print("✅ Login bem-sucedido")
            return jsonify(response_data), 200
        else:
            print("❌ Login falhou")
            return jsonify({
                "success": False,
                "error": "Email ou senha incorretos"
            }), 401
            
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/update_confg_maquina', methods=['POST'])
def update_machine_config():
    """Endpoint para atualizar configuração da máquina"""
    try:
        data = request.get_json()
        
        print(f"⚙️ Configuração recebida:")
        print(f"   Nome: {data.get('data', {}).get('Nome', 'N/A')}")
        print(f"   MAC: {data.get('data', {}).get('MAC', 'N/A')}")
        print(f"   Tipo: {data.get('data', {}).get('type', 'N/A')}")
        print(f"   Frequência: {data.get('data', {}).get('Frequency', 'N/A')}s")
        
        status = data.get('data', {}).get('status', {})
        print(f"   Status monitorados:")
        for key, value in status.items():
            if key != 'type':
                print(f"     {key}: {'✅' if value else '❌'}")
        
        return jsonify({
            "success": True,
            "message": "Configuração atualizada com sucesso"
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao processar configuração: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/maquina/status', methods=['PUT'])
def update_machine_status():
    """Endpoint para receber dados de monitoramento da máquina"""
    try:
        data = request.get_json()
        
        # Adicionar timestamp de recebimento
        data['received_at'] = datetime.now().isoformat()
        
        # Armazenar dados
        received_data.append(data)
        
        print(f"📊 Dados de monitoramento recebidos:")
        print(f"   Timestamp: {data.get('data', {}).get('timestamp', 'N/A')}")
        print(f"   Máquina: {data.get('data', {}).get('machine_info', {}).get('hostname', 'N/A')}")
        print(f"   MAC: {data.get('data', {}).get('machine_info', {}).get('mac_address', 'N/A')}")
        
        # Mostrar dados coletados
        system_data = data.get('data', {})
        if 'cpu' in system_data:
            print(f"   CPU: {system_data['cpu'].get('percentual_total', 'N/A')}%")
        if 'ram' in system_data:
            print(f"   RAM: {system_data['ram'].get('percentual', 'N/A')}%")
        if 'disco' in system_data:
            print(f"   Disco: {system_data['disco'].get('percentual', 'N/A')}%")
        if 'rede' in system_data:
            print(f"   Rede: ↑{system_data['rede'].get('bytes_enviados_mb', 'N/A')}MB ↓{system_data['rede'].get('bytes_recebidos_mb', 'N/A')}MB")
        if 'temperatura' in system_data:
            print(f"   Temperatura: {system_data['temperatura'].get('cpu', 'N/A')}°C")
        if 'top_5_processos_cpu' in system_data:
            processes = system_data['top_5_processos_cpu']
            print(f"   Top Processos: {len(processes)} processos")
        
        print(f"   Total de dados recebidos: {len(received_data)}")
        print("-" * 50)
        
        return jsonify({
            "success": True,
            "message": "Dados de monitoramento recebidos com sucesso",
            "received_at": data['received_at']
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Endpoint para verificar status do servidor"""
    return jsonify({
        "status": "running",
        "endpoints": {
            "login": "/api/login (POST)",
            "config": "/api/update_confg_maquina (POST)",
            "monitoring": "/api/maquina/status (PUT)",
            "health": "/api/status (GET)"
        },
        "data_received": len(received_data)
    })

@app.route('/api/data', methods=['GET'])
def get_received_data():
    """Endpoint para visualizar dados recebidos"""
    return jsonify({
        "total_received": len(received_data),
        "data": received_data[-10:] if received_data else []  # Últimos 10 registros
    })

if __name__ == '__main__':
    print("🚀 Servidor de teste completo iniciado!")
    print("📡 Endpoints disponíveis:")
    print("   🔐 Login: http://localhost:5000/api/login")
    print("   ⚙️ Config: http://localhost:5000/api/update_confg_maquina")
    print("   📊 Monitoramento: http://localhost:5000/api/maquina/status")
    print("   📈 Dados: http://localhost:5000/api/data")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
