"""
Script para testar o login diretamente
"""

import requests
import json
import platform
import socket
import uuid

def get_mac_address():
    """Obtém o endereço MAC da máquina"""
    try:
        # Obter MAC address
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                       for elements in range(0,2*6,2)][::-1])
        return mac.upper()
    except:
        return "00-00-00-00-00-00"

def get_username():
    """Obtém o nome do usuário atual"""
    try:
        return socket.gethostname()
    except:
        return "Unknown"

def get_operating_system():
    """Obtém informações do sistema operacional"""
    try:
        system = platform.system()
        release = platform.release()
        return f"{system} {release}"
    except:
        return "Unknown"

def test_login():
    """Testa o endpoint de login diretamente"""
    
    # URL do endpoint
    url = "https://wretched-casket-7vrr9w7rv5q5fxjp5-8000.app.github.dev/api/login"
    
    # Dados de teste
    email = "developer@rocks.com"
    password = "Dev@Rocks2025"
    mac_address = get_mac_address()
    username = get_username()
    operating_system = get_operating_system()
    
    # Payload
    payload = {
        "email": email,
        "password": password,
        "mac_address": mac_address,
        "username": username,
        "c": operating_system
    }
    
    print("🔐 Testando endpoint de login...")
    print(f"📡 URL: {url}")
    print(f"📧 Email: {email}")
    print(f"🔑 Senha: {password}")
    print(f"🖥️ MAC: {mac_address}")
    print(f"👤 Usuário: {username}")
    print(f"💻 SO: {operating_system}")
    print("-" * 50)
    
    try:
        # Fazer requisição POST
        response = requests.post(
            url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Rocks-Monitoramento-Desktop/1.0"
            },
            timeout=10
        )
        
        print(f"📤 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login bem-sucedido!")
            try:
                response_data = response.json()
                print(f"📥 Resposta: {json.dumps(response_data, indent=2)}")
            except:
                print(f"📥 Resposta: {response.text}")
        elif response.status_code == 401:
            print("❌ Credenciais inválidas")
            try:
                error_data = response.json()
                print(f"📥 Erro: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📥 Erro: {response.text}")
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
    test_login()
