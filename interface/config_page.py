"""
Página de configuração do sistema de monitoramento
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QGridLayout, QSlider, QSizePolicy, QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .widgets import ModernLineEdit, ModernButton, ToggleSwitch, CustomCheckBox
from .utils import get_logo_path, logo_exists

import logging
import os
logger = logging.getLogger(__name__)

class ConfigPage(QWidget):
    """Página de configuração"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)
        
        # Header com logo e ícone
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        if logo_exists():
            pixmap = QPixmap(get_logo_path())
            scaled_pixmap = pixmap.scaled(80, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("ROCKS")
            logo_label.setStyleSheet("""
                QLabel {
                    color: #FFFFFF;
                    font-size: 24px;
                    font-weight: bold;
                    font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
                }
            """)
        
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(logo_label)
        
        # Ícone do monitor (simulado com texto)
        self.monitor_icon = QLabel("🖥️")
        self.monitor_icon.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 32px;
            }
        """)
        self.monitor_icon.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header_layout.addWidget(self.monitor_icon)
        
        main_layout.addLayout(header_layout)
        
        # Campo Nome da máquina (sem label)
        self.machine_name_input = ModernLineEdit("Nome da máquina")
        main_layout.addWidget(self.machine_name_input)
        
        # Seção Status Monitorados
        status_label = QLabel("Selecionar status monitorados")
        status_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                font-weight: bold;
                margin-top: 10px;
                margin-bottom: 8px;
            }
        """)
        main_layout.addWidget(status_label)
        
        # Layout de 2 colunas usando QHBoxLayout
        checkbox_container = QHBoxLayout()
        checkbox_container.setSpacing(30)
        
        # Coluna esquerda
        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        
        # Coluna direita
        right_column = QVBoxLayout()
        right_column.setSpacing(20)
        
        # Primeira linha: CPU e RAM
        self.cpu_toggle = CustomCheckBox("CPU")
        self.cpu_toggle.setChecked(True)
        left_column.addWidget(self.cpu_toggle)
        
        self.ram_toggle = CustomCheckBox("RAM")
        self.ram_toggle.setChecked(True)
        right_column.addWidget(self.ram_toggle)
        
        # Segunda linha: DISCO e REDE
        self.disco_toggle = CustomCheckBox("DISCO")
        self.disco_toggle.setChecked(True)
        left_column.addWidget(self.disco_toggle)
        
        self.rede_toggle = CustomCheckBox("REDE")
        self.rede_toggle.setChecked(True)
        right_column.addWidget(self.rede_toggle)
        
        # Terceira linha: PROCESSOS e TEMPERATURA
        self.processos_toggle = CustomCheckBox("PROCESSOS")
        self.processos_toggle.setChecked(True)
        left_column.addWidget(self.processos_toggle)
        
        self.temperatura_toggle = CustomCheckBox("TEMPERATURA")
        self.temperatura_toggle.setChecked(True)
        right_column.addWidget(self.temperatura_toggle)
        
        # Adicionar as colunas ao container
        checkbox_container.addLayout(left_column)
        checkbox_container.addLayout(right_column)
        
        main_layout.addLayout(checkbox_container)
        
        # Espaçador entre checkboxes e frequência
        checkbox_spacer = QWidget()
        checkbox_spacer.setFixedHeight(15)
        main_layout.addWidget(checkbox_spacer)
        
        # Seção Frequência de atualização
        freq_label = QLabel("Frequência de atualização")
        freq_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                font-weight: bold;
                margin-top: 10px;
                margin-bottom: 8px;
            }
        """)
        main_layout.addWidget(freq_label)
        
        # Slider com labels
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(15)
        
        self.min_label = QLabel("1 segundo")
        self.min_label.setStyleSheet("""
            QLabel {
                color: #8E8E93;
                font-size: 14px;
            }
        """)
        self.min_label.setFixedWidth(80)
        slider_layout.addWidget(self.min_label)
        
        self.freq_slider = QSlider(Qt.Horizontal)
        self.freq_slider.setMinimum(1)
        self.freq_slider.setMaximum(10)
        self.freq_slider.setValue(1)
        self.freq_slider.valueChanged.connect(self.update_slider_label)
        self.freq_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background: #3A3A3A;
                border-radius: 3px;
                margin: 0 15px;
            }
            QSlider::sub-page:horizontal {
                background: #007AFF;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                border: none;
                width: 12px;
                height: 12px;
                border-radius: 6px;
                margin: -3px -6px;
            }
            QSlider::handle:horizontal:hover {
                background: #F0F0F0;
            }
        """)
        slider_layout.addWidget(self.freq_slider)
        
        max_label = QLabel("1-10 sec")
        max_label.setStyleSheet("""
            QLabel {
                color: #8E8E93;
                font-size: 14px;
            }
        """)
        max_label.setFixedWidth(80)
        max_label.setAlignment(Qt.AlignRight)
        slider_layout.addWidget(max_label)
        
        main_layout.addLayout(slider_layout)
        
        # Toggles
        # Notificar
        notify_layout = QHBoxLayout()
        notify_label = QLabel("Notificar")
        notify_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 400;
            }
        """)
        notify_layout.addWidget(notify_label)
        notify_layout.addStretch()
        
        self.notify_toggle = ToggleSwitch()
        self.notify_toggle.setChecked(True)
        notify_layout.addWidget(self.notify_toggle)
        
        main_layout.addLayout(notify_layout)
        
        # Iniciar com o SO
        startup_layout = QHBoxLayout()
        startup_label = QLabel("Iniciar com o SO")
        startup_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 400;
            }
        """)
        startup_layout.addWidget(startup_label)
        startup_layout.addStretch()
        
        self.startup_toggle = ToggleSwitch()
        self.startup_toggle.setChecked(False)
        startup_layout.addWidget(self.startup_toggle)
        
        main_layout.addLayout(startup_layout)
        
        # Espaçador
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)
        
        # Botão Concluído
        self.done_button = ModernButton("Concluído")
        self.done_button.clicked.connect(self.on_done_clicked)
        main_layout.addWidget(self.done_button)
        
    def update_slider_label(self):
        """Atualiza o texto do label do slider conforme o valor"""
        value = self.freq_slider.value()
        if value == 1:
            self.min_label.setText("1 segundo")
        else:
            self.min_label.setText(f"{value} segundos")
            
    def on_done_clicked(self):
        """Função chamada quando o botão concluído é clicado"""
        # Desabilitar botão e mostrar loading
        self.done_button.setEnabled(False)
        self.done_button.setText("Enviando...")
        
        # Coletar configurações
        self.config = {
            "machine_name": self.machine_name_input.text(),
            "monitored_status": {
                "cpu": self.cpu_toggle.isChecked(),
                "ram": self.ram_toggle.isChecked(),
                "disco": self.disco_toggle.isChecked(),
                "rede": self.rede_toggle.isChecked(),
                "processos": self.processos_toggle.isChecked(),
                "temperatura": self.temperatura_toggle.isChecked()
            },
            "update_frequency": self.freq_slider.value(),
            "notifications": self.notify_toggle.isChecked(),
            "start_with_os": self.startup_toggle.isChecked()
        }
        
        # Criar e iniciar worker para enviar configuração
        from .workers import ConfigUpdateWorker
        
        self.config_worker = ConfigUpdateWorker(self.config)
        self.config_worker.update_success.connect(self.on_config_success)
        self.config_worker.update_error.connect(self.on_config_error)
        self.config_worker.finished.connect(self.on_config_finished)
        self.config_worker.start()
    
    def on_config_success(self):
        """Callback chamado quando a configuração é enviada com sucesso"""
        logger.info("Configuração enviada com sucesso - iniciando monitoramento contínuo")
        
        # Iniciar monitoramento contínuo em segundo plano
        self.start_continuous_monitoring()
        
        # Fechar a aplicação
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()
    
    def start_continuous_monitoring(self):
        """Inicia o monitoramento contínuo em segundo plano"""
        try:
            import subprocess
            import sys
            
            # Iniciar o script de monitoramento em segundo plano
            script_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "scripts",
                "background_monitor.py",
            )

            if not os.path.exists(script_path):
                logger.error(
                    "Arquivo de monitoramento contínuo não encontrado: %s", script_path
                )
                return
            
            # Executar o script em processo separado
            if sys.platform.startswith('win'):
                # Windows - usar pythonw para executar sem console
                subprocess.Popen([sys.executable, script_path], 
                               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            else:
                # Linux/Mac
                subprocess.Popen([sys.executable, script_path],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            
            logger.info("Script de monitoramento iniciado em processo separado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar monitoramento contínuo: {e}")
    
    def on_monitoring_started(self):
        """Callback quando o monitoramento é iniciado"""
        logger.info("Monitoramento contínuo iniciado")
    
    def on_monitoring_stopped(self):
        """Callback quando o monitoramento é parado"""
        logger.info("Monitoramento contínuo parado")
    
    def on_monitoring_error(self, error: str):
        """Callback quando há erro no monitoramento"""
        logger.error(f"Erro no monitoramento contínuo: {error}")
    
    def on_data_sent(self):
        """Callback quando dados são enviados com sucesso"""
        logger.debug("Dados do sistema enviados com sucesso")
    
    def on_config_error(self, message):
        """Chamado quando há erro ao enviar configuração"""
        print(f"Erro ao enviar configuração: {message}")
        # Reabilitar botão
        self.done_button.setEnabled(True)
        self.done_button.setText("Concluído")
        
        # Mostrar mensagem de erro (opcional)
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Erro", f"Erro ao enviar configuração:\n{message}")
    
    def on_config_finished(self):
        """Chamado quando a thread de configuração termina"""
        if hasattr(self, 'config_worker') and self.config_worker:
            self.config_worker.deleteLater()
            self.config_worker = None
    
    def update_machine_icon(self):
        """Atualiza o ícone baseado no tipo de máquina"""
        try:
            from .utils import get_machine_icon_path, machine_icon_exists
            
            if machine_icon_exists():
                icon_path = get_machine_icon_path()
                
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.monitor_icon.setPixmap(scaled_pixmap)
                    # Limpar o texto e estilo se estava usando emoji
                    self.monitor_icon.setText("")
                    self.monitor_icon.setStyleSheet("")
                else:
                    # Fallback para emoji
                    self.monitor_icon.setText("🖥️")
                    self.monitor_icon.setStyleSheet("""
                        QLabel {
                            color: #FFFFFF;
                            font-size: 32px;
                        }
                    """)
                    self.monitor_icon.setPixmap(QPixmap())
            else:
                # Fallback para emoji se o arquivo não existir
                self.monitor_icon.setText("🖥️")
                self.monitor_icon.setStyleSheet("""
                    QLabel {
                        color: #FFFFFF;
                        font-size: 32px;
                    }
                """)
                self.monitor_icon.setPixmap(QPixmap())
        except Exception:
            # Fallback para emoji em caso de erro
            self.monitor_icon.setText("🖥️")
            self.monitor_icon.setStyleSheet("""
                QLabel {
                    color: #FFFFFF;
                    font-size: 32px;
                }
            """)
            self.monitor_icon.setPixmap(QPixmap())
