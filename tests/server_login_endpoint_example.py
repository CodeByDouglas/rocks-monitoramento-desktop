"""
Exemplo de implementação do endpoint de login para o servidor
Este é um exemplo que você pode usar como referência para implementar no seu servidor
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simulação de banco de dados de usuários
# Em produção, isso viria de um banco de dados real
USERS_DATABASE = {
    "teste@rocks.com": {
        "password": "123456",
        "name": "Usuário Teste",
        "machines": {
            "50-A1-32-1E-44-FC": {
                "name": "Máquina Teste",
                "type": "server",
                "config": {
                    "Frequency": 5,
                    "Notificar": True,
                    "iniciarSO": True,
                    "status": {
                        "CPU": False,
                        "DISCO": True,
                        "PROCESSO": True,
                        "RAM": True,
                        "REDE": False,
                        "TEMPERATURA": False
                    }
                }
            }
        }
    }
}

@app.route('/api/login', methods=['POST'])
def login():
    """
    Endpoint de login
    Recebe: email, password, mac_address, username, operating_system
    Retorna: dados da máquina se autenticação for bem-sucedida
    """
    try:
        data = request.get_json()
        
        # Extrair dados da requisição
        email = data.get('email', '')
        password = data.get('password', '')
        mac_address = data.get('mac_address', '')
        username = data.get('username', '')
        operating_system = data.get('operating_system', '')
        
        print(f"🔐 Tentativa de login:")
        print(f"   Email: {email}")
        print(f"   MAC: {mac_address}")
        print(f"   Username: {username}")
        print(f"   SO: {operating_system}")
        
        # Verificar se o usuário existe
        if email not in USERS_DATABASE:
            print("❌ Usuário não encontrado")
            return jsonify({
                "success": False,
                "error": "Email ou senha incorretos"
            }), 401
        
        user = USERS_DATABASE[email]
        
        # Verificar senha
        if user['password'] != password:
            print("❌ Senha incorreta")
            return jsonify({
                "success": False,
                "error": "Email ou senha incorretos"
            }), 401
        
        # Verificar se a máquina está registrada para este usuário
        if mac_address not in user['machines']:
            print("❌ Máquina não registrada para este usuário")
            return jsonify({
                "success": False,
                "error": "Máquina não autorizada"
            }), 403
        
        machine_data = user['machines'][mac_address]
        
        print("✅ Login bem-sucedido!")
        print(f"   Máquina: {machine_data['name']}")
        print(f"   Tipo: {machine_data['type']}")
        
        # Retornar dados da máquina
        response_data = {
            "success": True,
            "message": "Login realizado com sucesso",
            "data": {
                "Nome": machine_data['name'],
                "Notificar": machine_data['config']['Notificar'],
                "Frequency": machine_data['config']['Frequency'],
                "iniciarSO": machine_data['config']['iniciarSO'],
                "status": machine_data['config']['status']
            }
        }
        
        # Adicionar o tipo da máquina no status (se necessário)
        if 'type' not in response_data['data']['status']:
            response_data['data']['status']['type'] = machine_data['type']
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/update_confg_maquina', methods=['POST'])
def update_machine_config():
    """
    Endpoint para atualizar configuração da máquina
    Recebe: dados da configuração
    Retorna: confirmação de atualização
    """
    try:
        data = request.get_json()
        
        print(f"⚙️ Atualização de configuração recebida:")
        print(f"   Nome: {data.get('data', {}).get('Nome', 'N/A')}")
        print(f"   MAC: {data.get('data', {}).get('MAC', 'N/A')}")
        print(f"   Tipo: {data.get('data', {}).get('type', 'N/A')}")
        print(f"   Frequência: {data.get('data', {}).get('Frequency', 'N/A')}s")
        
        # Aqui você salvaria a configuração no banco de dados
        # Por enquanto, apenas retornamos sucesso
        
        return jsonify({
            "success": True,
            "message": "Configuração atualizada com sucesso"
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao atualizar configuração: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/maquina/status', methods=['PUT'])
def update_machine_status():
    """
    Endpoint para receber dados de monitoramento da máquina
    Recebe: dados de monitoramento do sistema
    Retorna: confirmação de recebimento
    """
    try:
        data = request.get_json()
        
        print(f"📊 Dados de monitoramento recebidos:")
        print(f"   Timestamp: {data.get('data', {}).get('timestamp', 'N/A')}")
        print(f"   Máquina: {data.get('data', {}).get('machine_info', {}).get('hostname', 'N/A')}")
        print(f"   MAC: {data.get('data', {}).get('machine_info', {}).get('mac_address', 'N/A')}")
        
        # Aqui você salvaria os dados de monitoramento no banco de dados
        # Por enquanto, apenas retornamos sucesso
        
        return jsonify({
            "success": True,
            "message": "Status recebido"
        }), 200
        
    except Exception as e:
        print(f"❌ Erro ao processar status: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "login": "/api/login (POST)",
            "config": "/api/update_confg_maquina (POST)",
            "monitoring": "/api/maquina/status (PUT)",
            "health": "/api/health (GET)"
        }
    })

if __name__ == '__main__':
    print("🚀 Servidor de exemplo iniciado!")
    print("📡 Endpoints disponíveis:")
    print("   🔐 Login: http://localhost:5000/api/login")
    print("   ⚙️ Config: http://localhost:5000/api/update_confg_maquina")
    print("   📊 Monitoramento: http://localhost:5000/api/maquina/status")
    print("   📈 Health: http://localhost:5000/api/health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
