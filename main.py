import sys
from PyQt6.QtWidgets import QApplication
from config_generator import ConfigGenerator

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConfigGenerator()
    window.update_ui_from_config()
    window.show()
    sys.exit(app.exec())