"""
Janela principal do sistema de monitoramento
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QStackedWidget, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .login_page import LoginPage
from .config_page import ConfigPage

class MainWindow(QMainWindow):
    """Janela principal do sistema"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Rocks - Sistema de Monitoramento")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Container do formulário
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_container.setStyleSheet("""
            #formContainer {
                background-color: #000000;
                border-radius: 20px;
                border: 1px solid #333333;
            }
        """)
        
        container_layout = QVBoxLayout(form_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Stacked widget para gerenciar as páginas
        self.stacked_widget = QStackedWidget()
        container_layout.addWidget(self.stacked_widget)
        
        # Criar as páginas
        self.login_page = LoginPage(self)
        self.config_page = ConfigPage(self)
        
        # Adicionar páginas ao stacked widget
        self.stacked_widget.addWidget(self.login_page)  # índice 0
        self.stacked_widget.addWidget(self.config_page)  # índice 1
        
        main_layout.addWidget(form_container)
        
        # Configurar fonte da aplicação
        app = QApplication.instance()
        if app:
            font = QFont("SF Pro Display", 10)
            app.setFont(font)
        
        # Centralizar a janela
        self.center_window()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def show_config_page(self, data):
        """Mostra a página de configuração com os dados recebidos"""
        # Redimensionar a janela para a tela de configuração
        self.setFixedSize(480, 800)
        self.center_window()
        
        # Preencher os dados recebidos do servidor
        if 'data' in data:
            machine_data = data['data']
            
            # Nome da máquina
            if 'Nome' in machine_data:
                self.config_page.machine_name_input.setText(machine_data['Nome'])
            
            # Frequência de atualização
            if 'Frequency' in machine_data:
                self.config_page.freq_slider.setValue(machine_data['Frequency'])
            
            # Notificações
            if 'Notificar' in machine_data:
                self.config_page.notify_toggle.setChecked(machine_data['Notificar'])
            
            # Iniciar com SO
            if 'iniciarSO' in machine_data:
                self.config_page.startup_toggle.setChecked(machine_data['iniciarSO'])
            
            # Status monitorados
            if 'status' in machine_data:
                status_data = machine_data['status']
                
                # Mapeamento dos status para os toggles
                status_mapping = {
                    'CPU': self.config_page.cpu_toggle,
                    'RAM': self.config_page.ram_toggle,
                    'DISCO': self.config_page.disco_toggle,
                    'REDE': self.config_page.rede_toggle,
                    'PROCESSO': self.config_page.processos_toggle,
                    'TEMPERATURA': self.config_page.temperatura_toggle
                }
                
                # Aplicar os valores recebidos
                for status_name, checkbox in status_mapping.items():
                    if status_name in status_data:
                        checkbox.setChecked(status_data[status_name])
        
        # Mudar para a página de configuração
        self.stacked_widget.setCurrentIndex(1)
        
        # Atualizar o ícone da página de configuração após o login
        self.update_config_page_icon()
        
    def update_config_page_icon(self):
        """Atualiza o ícone da página de configuração baseado no tipo de máquina"""
        try:
            self.config_page.update_machine_icon()
        except Exception as e:
            print(f"Erro ao atualizar ícone: {e}")
        
    def mousePressEvent(self, event):
        """Evento de clique do mouse - só permite arrastar na parte superior"""
        if event.button() == Qt.LeftButton:
            # Verificar se o clique foi na parte superior da janela (primeiros 50 pixels)
            if event.position().y() <= 50:
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()
            else:
                # Se não foi na parte superior, não permitir arraste
                event.ignore()
        else:
            super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """Evento de movimento do mouse - só arrasta se foi iniciado na parte superior"""
        if (event.buttons() == Qt.LeftButton and 
            hasattr(self, 'drag_position') and 
            self.drag_position is not None):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
        else:
            super().mouseMoveEvent(event)
