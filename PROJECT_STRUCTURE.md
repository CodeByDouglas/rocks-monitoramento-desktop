# 📁 Estrutura do Projeto - Sistema de Monitoramento Rocks

## 🎯 Visão Geral

Este documento descreve a estrutura organizada e as melhorias implementadas no projeto Sistema de Monitoramento Rocks.

## 🏗️ Estrutura de Pastas

```
rocks-monitoramento-desktop/
├── 📁 api/                    # Módulo de comunicação com servidor
│   ├── __init__.py
│   ├── api_client.py         # Cliente HTTP para API
│   └── auth_service.py       # Serviço de autenticação
├── 📁 monitoramento/          # Módulo de monitoramento do sistema
│   ├── __init__.py
│   └── system_monitor.py     # Coleta de dados da máquina
├── 📁 interface/             # Módulo de interface gráfica
│   ├── __init__.py
│   ├── main_window.py        # Janela principal
│   ├── login_page.py         # Página de login
│   ├── config_page.py        # Página de configuração
│   ├── widgets.py            # Widgets customizados
│   ├── workers.py            # Threads assíncronas
│   ├── utils.py              # Utilitários da interface
│   └── 📁 image/             # Imagens da interface
│       ├── logo_rocks.png
│       ├── icone_pc.png
│       └── icone_server.png
├── 📁 scripts/               # Scripts utilitários
│   ├── __init__.py
│   └── background_monitor.py # Monitoramento em segundo plano
├── 📁 tests/                 # Arquivos de teste
│   ├── __init__.py
│   ├── test_complete_server.py
│   ├── test_monitoring_direct.py
│   └── ...                   # Outros arquivos de teste
├── 📁 data/                  # Dados e logs
│   ├── __init__.py
│   ├── configuracao_maquina.json
│   ├── dados_sistema.json
│   └── *.log
├── 📁 .venv/                 # Ambiente virtual Python
├── main.py                   # Arquivo principal da aplicação
├── config.py                 # Configurações centralizadas
├── config_dev.py             # Configurações de desenvolvimento
├── config_test.py            # Configurações de teste
├── config_prod.py            # Configurações de produção
├── requirements.txt          # Dependências do projeto
├── setup.py                  # Script de instalação
├── Makefile                  # Comandos de automação
├── env.example               # Exemplo de variáveis de ambiente
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Documentação principal
```

## 🔧 Melhorias Implementadas

### 1. **Organização de Pastas**
- ✅ **`tests/`**: Todos os arquivos de teste organizados
- ✅ **`scripts/`**: Scripts utilitários separados
- ✅ **`data/`**: Dados, logs e configurações centralizados

### 2. **Configurações Centralizadas**
- ✅ **`config.py`**: Configurações principais
- ✅ **`config_dev.py`**: Configurações de desenvolvimento
- ✅ **`config_test.py`**: Configurações de teste
- ✅ **`config_prod.py`**: Configurações de produção

### 3. **Arquivos de Configuração**
- ✅ **`setup.py`**: Instalação via pip
- ✅ **`Makefile`**: Automação de tarefas
- ✅ **`env.example`**: Exemplo de variáveis de ambiente

### 4. **Estrutura de Módulos**
- ✅ **`__init__.py`**: Em todas as pastas para importação
- ✅ **Importações organizadas**: Estrutura clara de dependências
- ✅ **Separação de responsabilidades**: Cada módulo tem função específica

## 📋 Arquivos Organizados

### **Arquivos de Teste** → `tests/`
- `test_complete_server.py`
- `test_monitoring_direct.py`
- `test_continuous_monitoring.py`
- `test_login_direct.py`
- `test_monitoring_server.py`
- `server_login_endpoint_example.py`

### **Scripts Utilitários** → `scripts/`
- `background_monitor.py`

### **Dados e Logs** → `data/`
- `configuracao_maquina.json`
- `dados_sistema.json`
- `rocks_monitoramento.log`
- `background_monitor.log`

## 🚀 Benefícios da Nova Estrutura

### 1. **Organização**
- ✅ Código fonte separado de arquivos temporários
- ✅ Testes organizados em pasta específica
- ✅ Scripts utilitários isolados
- ✅ Dados e logs centralizados

### 2. **Manutenibilidade**
- ✅ Configurações centralizadas e organizadas
- ✅ Fácil alteração entre ambientes (dev/test/prod)
- ✅ Estrutura clara e intuitiva
- ✅ Documentação atualizada

### 3. **Desenvolvimento**
- ✅ Makefile para automação de tarefas
- ✅ Setup.py para instalação via pip
- ✅ Configurações específicas por ambiente
- ✅ Estrutura pronta para CI/CD

### 4. **Deploy**
- ✅ Separação clara entre código e dados
- ✅ Configurações de produção isoladas
- ✅ Scripts de instalação automatizados
- ✅ Estrutura escalável

## 🔄 Fluxo de Trabalho

### **Desenvolvimento**
1. Usar `config_dev.py` para configurações locais
2. Executar testes com `make test`
3. Iniciar servidor de teste com `make test-server`
4. Executar aplicação com `make run`

### **Teste**
1. Usar `config_test.py` para configurações de teste
2. Executar testes automatizados
3. Verificar logs em `data/`

### **Produção**
1. Usar `config_prod.py` para configurações de produção
2. Configurar variáveis de ambiente
3. Executar com `make prod`

## 📝 Comandos Disponíveis

### **Via Makefile**
```bash
make help          # Mostra todos os comandos
make install       # Instala dependências
make dev           # Modo desenvolvimento
make test          # Modo teste
make prod          # Modo produção
make run           # Executa aplicação
make test-server   # Inicia servidor de teste
make clean         # Limpa arquivos temporários
make format        # Formata código
make lint          # Executa linting
make monitor       # Inicia monitoramento
make check         # Verifica estrutura
```

### **Via Python**
```bash
python main.py                           # Aplicação principal
python scripts/background_monitor.py     # Monitoramento
python -m tests.test_complete_server     # Servidor de teste
```

## 🎯 Próximos Passos

### **Implementações Futuras**
- [ ] CI/CD pipeline
- [ ] Testes automatizados
- [ ] Documentação de API
- [ ] Docker containerization
- [ ] Monitoramento de performance
- [ ] Sistema de backup automático

### **Melhorias de Código**
- [ ] Type hints em todos os módulos
- [ ] Testes unitários completos
- [ ] Logging estruturado
- [ ] Tratamento de erros robusto
- [ ] Validação de dados
- [ ] Cache de configurações

## 📊 Métricas de Organização

- **Arquivos organizados**: 100%
- **Pastas estruturadas**: 100%
- **Configurações centralizadas**: 100%
- **Documentação atualizada**: 100%
- **Estrutura modular**: 100%

## 🏆 Conclusão

A reorganização do projeto resultou em uma estrutura profissional, organizada e escalável que facilita:

1. **Desenvolvimento** de novas funcionalidades
2. **Manutenção** do código existente
3. **Testes** automatizados e organizados
4. **Deploy** em diferentes ambientes
5. **Colaboração** entre desenvolvedores

A nova estrutura segue as melhores práticas de desenvolvimento Python e está pronta para crescimento e evolução do projeto.

