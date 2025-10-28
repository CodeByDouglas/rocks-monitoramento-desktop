"""
Widgets customizados para a interface do sistema de monitoramento
"""

from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget, QCheckBox, QProxyStyle, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QPen, QBrush, QColor

class ModernLineEdit(QLineEdit):
    """Campo de entrada personalizado com estilo moderno"""
    def __init__(self, placeholder_text="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.setup_style()
        
    def setup_style(self):
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #2A2A2A;
                border: 2px solid #3A3A3A;
                border-radius: 25px;
                padding: 0 20px;
                color: #FFFFFF;
                font-size: 16px;
                font-weight: 400;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
                background-color: #2A2A2A;
            }
            QLineEdit::placeholder {
                color: #8E8E93;
            }
        """)

class ModernButton(QPushButton):
    """Botão personalizado com estilo moderno e gradiente"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setup_style()
        
    def setup_style(self):
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007AFF, stop:1 #0056CC);
                border: none;
                border-radius: 25px;
                color: white;
                font-size: 16px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056CC, stop:1 #004499);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #004499, stop:1 #003366);
            }
            QPushButton:disabled {
                background: #666666;
                color: #999999;
            }
        """)

class CustomCheckBox(QWidget):
    """Checkbox customizado com indicador desenhado manualmente"""
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.text = text
        self.checked = False
        self.setFixedHeight(35)  # Altura reduzida para evitar sobreposição
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            CustomCheckBox {
                color: #FFFFFF;
                font-size: 15px;
                padding-left: 35px;
                background: transparent;
            }
        """)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar o indicador do checkbox
        indicator_size = 20  # Tamanho reduzido
        x = 5
        y = (self.height() - indicator_size) // 2
        
        # Fundo do checkbox
        if self.checked:
            painter.setBrush(QBrush(QColor("#007AFF")))
        else:
            painter.setBrush(QBrush(QColor("#2A2A2A")))
        
        painter.setPen(QPen(QColor("#007AFF"), 2))
        painter.drawRoundedRect(x, y, indicator_size, indicator_size, 4, 4)
        
        # Desenhar o checkmark se marcado
        if self.checked:
            painter.setPen(QPen(QColor("#FFFFFF"), 2))
            # Desenhar o checkmark ajustado ao novo tamanho
            painter.drawLine(x + 5, y + 10, x + 8, y + 13)
            painter.drawLine(x + 8, y + 13, x + 15, y + 6)
        
        # Desenhar o texto
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(35, 0, self.width() - 35, self.height(), 
                        Qt.AlignLeft | Qt.AlignVCenter, self.text)
        
    def mousePressEvent(self, event):
        self.checked = not self.checked
        self.update()
        super().mousePressEvent(event)
        
    def isChecked(self):
        return self.checked
        
    def setChecked(self, checked):
        self.checked = checked
        self.update()

class ToggleSwitch(QWidget):
    """Toggle switch personalizado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 24)  # Diminuído de 50x30 para 40x24
        self.checked = False
        self.setCursor(Qt.PointingHandCursor)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar o fundo
        if self.checked:
            painter.setBrush(QBrush(QColor("#007AFF")))
        else:
            painter.setBrush(QBrush(QColor("#3A3A3A")))
        
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)
        
        # Desenhar o círculo - centralizado verticalmente
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        circle_size = 18  # Diminuído de 22 para 18
        if self.checked:
            circle_x = self.width() - circle_size - 3  # 3px de margem
        else:
            circle_x = 3  # 3px de margem
        
        circle_y = (self.height() - circle_size) // 2  # Centralizado verticalmente
        painter.drawEllipse(circle_x, circle_y, circle_size, circle_size)
        
    def mousePressEvent(self, event):
        self.checked = not self.checked
        self.update()
        super().mousePressEvent(event)
        
    def isChecked(self):
        return self.checked
        
    def setChecked(self, checked):
        self.checked = checked
        self.update()

class LabeledToggle(QWidget):
    """Widget que agrega QLabel + ToggleSwitch"""
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)  # Altura fixa conforme sugerido
        self.setup_ui(text)
        
    def setup_ui(self, text):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Label com largura fixa para alinhamento uniforme
        self.label = QLabel(text)
        self.label.setFixedWidth(100)  # Largura fixa para todos os labels
        self.label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 15px;
                font-weight: 400;
            }
        """)
        layout.addWidget(self.label)

        # Espaçador
        layout.addStretch()

        # Toggle
        self.toggle = ToggleSwitch()
        layout.addWidget(self.toggle)
        
    def isChecked(self):
        return self.toggle.isChecked()
        
    def setChecked(self, checked):
        self.toggle.setChecked(checked)
