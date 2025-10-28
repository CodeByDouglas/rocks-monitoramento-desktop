# Sistema de Monitoramento Rocks - Desktop

Sistema de monitoramento de máquinas com interface gráfica moderna e comunicação com servidor.

## 📁 Estrutura do Projeto

```
rocks-monitoramento-desktop/
├── api/                    # Módulo de comunicação com servidor
│   ├── __init__.py
│   ├── api_client.py      # Cliente HTTP para API
│   └── auth_service.py    # Serviço de autenticação
├── monitoramento/          # Módulo de monitoramento do sistema
│   ├── __init__.py
│   └── system_monitor.py  # Coleta de dados da máquina
├── interface/             # Módulo de interface gráfica
│   ├── __init__.py
│   ├── main_window.py    # Janela principal
│   ├── login_page.py     # Página de login
│   ├── config_page.py    # Página de configuração
│   ├── widgets.py        # Widgets customizados
│   ├── workers.py        # Threads assíncronas
│   ├── utils.py          # Utilitários da interface
│   └── image/            # Imagens da interface
│       ├── logo_rocks.png
│       ├── icone_pc.png
│       └── icone_server.png
├── scripts/               # Scripts utilitários
│   ├── __init__.py
│   └── background_monitor.py  # Monitoramento em segundo plano
├── tests/                 # Arquivos de teste
│   ├── __init__.py
│   ├── test_complete_server.py
│   ├── test_monitoring_direct.py
│   └── ...               # Outros arquivos de teste
├── data/                  # Dados e logs
│   ├── __init__.py
│   ├── configuracao_maquina.json
│   ├── dados_sistema.json
│   └── *.log
├── main.py               # Arquivo principal
├── config.py             # Configurações centralizadas
├── requirements.txt      # Dependências
└── README.md            # Documentação
```

## 🚀 Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd rocks-monitoramento-desktop
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual:**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Funcionalidades

### 📊 Monitoramento do Sistema
- **Sistema Operacional**: Informações detalhadas (Windows, Linux, macOS)
- **CPU**: Percentual de uso, uso por núcleo, número de núcleos
- **RAM**: Total, disponível, usado, percentual
- **Disco**: Espaço total, usado, livre, percentual
- **Rede**: Bytes enviados/recebidos
- **Temperatura**: Temperatura do CPU
- **Processos**: Top 5 processos que mais consomem CPU

### 🔐 Autenticação
- Login com email e senha
- Identificação automática da máquina (MAC address, hostname, sistema operacional)
- Comunicação segura com servidor

### ⚙️ Configuração
- Nome da máquina
- Status monitorados (CPU, RAM, Disco, Rede, Processos, Temperatura)
- Frequência de atualização (1-10 segundos)
- Notificações (ativar/desativar)
- Iniciar com sistema operacional
- **Envio automático**: Configuração é enviada ao servidor quando o usuário clica em "Concluído"

## 🏗️ Arquitetura

### 1. Módulo de Monitoramento (`monitoramento/`)
Responsável por coletar dados da máquina usando `psutil`:
- `SystemMonitor`: Classe principal para coleta de dados
- Tratamento de erros robusto
- Logging detalhado

### 2. Módulo de API (`api/`)
Responsável pela comunicação com o servidor:
- `APIClient`: Cliente HTTP para requisições
- `AuthService`: Gerenciamento de autenticação
- Tratamento de erros de rede

### 3. Módulo de Interface (`interface/`)
Responsável pela interface gráfica:
- Design moderno estilo iOS
- Widgets customizados
- Threads assíncronas para operações de rede
- Navegação entre páginas

### 4. Configurações Centralizadas (`config.py`)
Arquivo central com todas as configurações:
- URLs da API
- Configurações de logging
- Configurações da interface
- Caminhos de arquivos
- Configurações de monitoramento

### 5. Scripts Utilitários (`scripts/`)
Scripts para operações específicas:
- `background_monitor.py`: Monitoramento contínuo em segundo plano

## 📡 Endpoints da API

### Autenticação
- **POST** `/api/login` - Login do usuário
  - **Body**: `{"email": "...", "password": "...", "mac_address": "...", "username": "...", "operating_system": "..."}`
  - **Resposta 200**: Dados da máquina para configuração
  - **Resposta 401**: Credenciais inválidas

### Configuração
- **POST** `/api/update_confg_maquina` - Atualizar configuração da máquina
  - **Body**: `{"data": {"Nome": "...", "MAC": "...", "type": "...", "Notificar": true, "Frequency": 5, "iniciarSO": false, "status": {...}}}`
  - **Resposta 200**: Configuração atualizada com sucesso

### Monitoramento
- **PUT** `/api/maquina/status` - Enviar dados de monitoramento
  - **Body**: `{"data": {...}}` (dados do sistema coletados)
  - **Resposta 200**: Dados recebidos com sucesso

## 🔄 Fluxo de Funcionamento

1. **Login**: Usuário insere credenciais → Sistema coleta dados da máquina → Envia para API → Recebe configuração
2. **Configuração**: Interface preenche com dados recebidos → Usuário ajusta configurações → Clica em "Concluído"
3. **Envio**: Configuração é enviada para API → Salva localmente em `data/configuracao_maquina.json`
4. **Monitoramento**: Script de background é iniciado → Coleta dados continuamente → Envia para API
5. **Persistência**: Monitoramento continua rodando mesmo após fechar a interface

## 📁 Estrutura de Arquivos

### Arquivos de Configuração
- **`configuracao_maquina.json`**: Configuração da máquina (localizado em `data/`)
  - **Formato do arquivo:** `configuracao_maquina.json` (sempre o mesmo arquivo, atualizado a cada nova configuração)
  - **Estrutura**:
    ```json
    {
      "timestamp": "2025-08-29T14:43:41.312270",
      "machine_info": {
        "hostname": "Nome da Máquina",
        "mac_address": "XX-XX-XX-XX-XX-XX",
        "operating_system": "Windows 11 (11)",
        "type": "server"
      },
      "configuration": {
        "machine_name": "Nome Personalizado",
        "monitored_status": {
          "cpu": true,
          "ram": true,
          "disco": true,
          "rede": true,
          "processos": true,
          "temperatura": true
        },
        "update_frequency": 10,
        "notifications": true,
        "start_with_os": true
      }
    }
    ```

### Arquivos de Dados
- **`dados_sistema.json`**: Dados coletados do sistema (localizado em `data/`)
- **`*.log`**: Arquivos de log (localizados em `data/`)

## 🎨 Interface Gráfica

### Design
- **Estilo**: iOS/Material Design
- **Cores**: Tema escuro com azul como cor primária
- **Fontes**: SF Pro Display (fallback: Segoe UI)

### Páginas
1. **Login**: Email, senha e botão de continuar
2. **Configuração**: Formulário completo com todos os parâmetros

### Widgets Customizados
- **`ModernLineEdit`**: Campo de texto estilizado
- **`ModernButton`**: Botão com design moderno
- **`ToggleSwitch`**: Switch estilo iOS
- **`CustomCheckBox`**: Checkbox personalizado

## 🔧 Configuração

### Variáveis de Ambiente
- **`ROCKS_API_URL`**: URL base da API (padrão: servidor de teste)
- **`ROCKS_LOG_LEVEL`**: Nível de logging (padrão: INFO)

### Configurações de Desenvolvimento
- **Servidor de teste**: `test_complete_server.py` (pasta `tests/`)
- **Logs**: Configuráveis via `config.py`
- **Timeouts**: Configuráveis para desenvolvimento

## 🚀 Execução

### Aplicação Principal
```bash
python main.py
```

### Monitoramento em Background
```bash
python scripts/background_monitor.py
```

### Servidor de Teste
```bash
cd tests
python test_complete_server.py
```

## 📝 Logging

O sistema utiliza logging estruturado com:
- **Nível configurável** (INFO por padrão)
- **Arquivo de log** em `data/rocks_monitoramento.log`
- **Console output** para desenvolvimento
- **Formato padronizado** com timestamp e contexto

## 🐛 Troubleshooting

### Problemas Comuns
1. **Erro de conexão**: Verificar se o servidor está acessível
2. **Arquivo não encontrado**: Verificar se as pastas `data/` e `scripts/` existem
3. **Erro de importação**: Verificar se o ambiente virtual está ativo

### Logs
- **Aplicação principal**: `data/rocks_monitoramento.log`
- **Monitoramento**: `data/background_monitor.log`
- **Console**: Logs em tempo real durante execução

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.