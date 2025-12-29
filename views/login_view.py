# views/login_view.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

# from services.login import check_credentials # Definir mejor


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ingreso al Sistema")
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Widgets
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        
        btn_login = QPushButton("Ingresar")
        btn_login.clicked.connect(self.check_login)

        # Layout
        layout.addWidget(QLabel("Bienvenido al Gestor de Tareas"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(btn_login)
        
        self.setLayout(layout)

    def check_login(self):
        # Lógica simple para prototipo
        if self.user_input.text()and self.pass_input.text():
            self.accept() # Cierra el dialogo y retorna QDialog.Accepted
        else:
            self.accept()
            #QMessageBox.warning(self, "Error", "Por favor ingrese credenciales")
            