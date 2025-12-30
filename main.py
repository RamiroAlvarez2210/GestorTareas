# main.py
import sys
from PyQt5.QtWidgets import QApplication
from views.login_view import LoginWindow
from views.dashboard_view import MainWindow

from views.options_view import OptionsWindow

def main():
    app = QApplication(sys.argv)
    
    # Estilo básico para generalizar la apariencia (Fusion es limpio y estándar)
    app.setStyle("Fusion") 
    
    # 1. Mostrar Login
    login = LoginWindow()
    if login.exec_() == login.Accepted:
        # 2. Si el login es correcto, mostrar Dashboard
        window = OptionsWindow() #MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()
    