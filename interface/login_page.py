"""
Página de login do sistema de monitoramento
"""

import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .widgets import ModernLineEdit, ModernButton
from .workers import LoginWorker
from .utils import get_mac_address, get_username, get_logo_path, logo_exists

class LoginPage(QWidget):
    """Página de login"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.login_worker = None
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)
        
        # Logo
        logo_label = QLabel()
        if logo_exists():
            pixmap = QPixmap(get_logo_path())
            # Redimensionar logo mantendo proporção
            scaled_pixmap = pixmap.scaled(120, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Fallback para texto se logo não existir
            logo_label.setText("ROCKS")
            logo_label.setStyleSheet("""
                QLabel {
                    color: #FFFFFF;
                    font-size: 32px;
                    font-weight: bold;
                    font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
                }
            """)
        
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)
        
        # Espaçador
        spacer1 = QWidget()
        spacer1.setFixedHeight(20)
        main_layout.addWidget(spacer1)
        
        # Campo de email
        self.email_input = ModernLineEdit("Email")
        main_layout.addWidget(self.email_input)
        
        # Campo de senha
        self.password_input = ModernLineEdit("Senha")
        self.password_input.setEchoMode(ModernLineEdit.Password)
        main_layout.addWidget(self.password_input)
        
        # Label de erro (inicialmente oculto)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("""
            QLabel {
                color: #FF3B30;
                font-size: 14px;
                text-align: center;
                padding: 5px;
            }
        """)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        main_layout.addWidget(self.error_label)
        
        # Espaçador
        spacer2 = QWidget()
        spacer2.setFixedHeight(10)
        main_layout.addWidget(spacer2)
        
        # Botão continuar
        self.continue_button = ModernButton("Continuar")
        self.continue_button.clicked.connect(self.on_continue_clicked)
        main_layout.addWidget(self.continue_button)
        
    def show_error(self, message):
        """Mostra mensagem de erro"""
        self.error_label.setText(message)
        self.error_label.show()
        self.continue_button.setEnabled(True)
        self.continue_button.setText("Continuar")
        
    def hide_error(self):
        """Esconde mensagem de erro"""
        self.error_label.hide()
        
    def on_continue_clicked(self):
        """Função chamada quando o botão continuar é clicado"""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validação básica
        if not email or not password:
            self.show_error("Por favor, preencha email e senha")
            return
        
        # Esconder erro anterior
        self.hide_error()
        
        # Desabilitar botão e mostrar loading
        self.continue_button.setEnabled(False)
        self.continue_button.setText("Autenticando...")
        
        # Criar e iniciar thread de login
        self.login_worker = LoginWorker(email, password)
        self.login_worker.login_success.connect(self.on_login_success)
        self.login_worker.login_error.connect(self.on_login_error)
        self.login_worker.network_error.connect(self.on_network_error)
        self.login_worker.finished.connect(self.on_login_finished)
        self.login_worker.start()
        
    def on_login_success(self, data):
        """Chamado quando o login é bem-sucedido"""
        print("Login bem-sucedido!")
        print(f"Dados recebidos: {json.dumps(data, indent=2)}")
        
        # Notificar o parent (MainWindow) para trocar para a página de configuração
        if self.parent:
            self.parent.show_config_page(data)
        
    def on_login_error(self, message):
        """Chamado quando há erro de autenticação"""
        print(f"Erro de login: {message}")
        self.show_error(message)
        
    def on_network_error(self, message):
        """Chamado quando há erro de rede"""
        print(f"Erro de rede: {message}")
        self.show_error(message)
        
    def on_login_finished(self):
        """Chamado quando a thread de login termina"""
        if self.login_worker:
            self.login_worker.deleteLater()
            self.login_worker = None
