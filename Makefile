# Makefile para o Sistema de Monitoramento Rocks

.PHONY: help install dev test prod clean run test-server

# Variáveis
PYTHON = python
PIP = pip
VENV = .venv
PYTHON_VENV = $(VENV)/Scripts/python
PIP_VENV = $(VENV)/Scripts/pip

# Comandos padrão
help:
	@echo "Sistema de Monitoramento Rocks - Comandos disponíveis:"
	@echo ""
	@echo "  install     - Instala dependências"
	@echo "  dev         - Executa em modo desenvolvimento"
	@echo "  test        - Executa em modo teste"
	@echo "  prod        - Executa em modo produção"
	@echo "  run         - Executa aplicação principal"
	@echo "  test-server - Inicia servidor de teste"
	@echo "  clean       - Limpa arquivos temporários"
	@echo "  format      - Formata código com black"
	@echo "  lint        - Executa linting com flake8"

# Instalação
install:
	@echo "Instalando dependências..."
	$(PYTHON) -m venv $(VENV)
	$(PIP_VENV) install -r requirements.txt
	@echo "Dependências instaladas com sucesso!"

# Desenvolvimento
dev:
	@echo "Executando em modo desenvolvimento..."
	$(PYTHON_VENV) -c "import config_dev; print('Configuração de desenvolvimento carregada')"

# Teste
test:
	@echo "Executando em modo teste..."
	$(PYTHON_VENV) -c "import config_test; print('Configuração de teste carregada')"

# Produção
prod:
	@echo "Executando em modo produção..."
	$(PYTHON_VENV) -c "import config_prod; print('Configuração de produção carregada')"

# Executar aplicação
run:
	@echo "Iniciando aplicação..."
	$(PYTHON_VENV) main.py

# Servidor de teste
test-server:
	@echo "Iniciando servidor de teste..."
	cd tests && $(PYTHON_VENV) test_complete_server.py

# Limpeza
clean:
	@echo "Limpando arquivos temporários..."
	rm -rf __pycache__/
	rm -rf */__pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	@echo "Limpeza concluída!"

# Formatação de código
format:
	@echo "Formatando código..."
	$(PIP_VENV) install black
	$(PYTHON_VENV) -m black .

# Linting
lint:
	@echo "Executando linting..."
	$(PIP_VENV) install flake8
	$(PYTHON_VENV) -m flake8 .

# Monitoramento em background
monitor:
	@echo "Iniciando monitoramento em background..."
	$(PYTHON_VENV) scripts/background_monitor.py

# Verificar estrutura
check:
	@echo "Verificando estrutura do projeto..."
	@echo "📁 Estrutura atual:"
	@tree -I '__pycache__|.venv|.git' -a

