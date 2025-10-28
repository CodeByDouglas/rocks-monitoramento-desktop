"""
Sistema de Monitoramento Rocks - Arquivo Principal
"""

import sys
import logging
from PySide6.QtWidgets import QApplication

from config import LOGGING_CONFIG
from interface.main_window import MainWindow

# Configurar logging usando as configurações centralizadas
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOGGING_CONFIG["file"], encoding=LOGGING_CONFIG["encoding"])
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Função principal da aplicação"""
    try:
        app = QApplication(sys.argv)
        
        # Configurar estilo global da aplicação
        app.setStyle("Fusion")
        
        logger.info("Iniciando aplicação de monitoramento Rocks")
        
        # Criar e mostrar a janela principal
        main_window = MainWindow()
        main_window.show()
        
        logger.info("Aplicação iniciada com sucesso")
        
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
