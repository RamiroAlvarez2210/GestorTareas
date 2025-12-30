''' 
from PyQt5.QtWidgets import (QMainWindow,QLabel,QPushButton)


class OptionsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.resize(400, 300)
        # Aquí iría la implementación de la ventana de opciones
        self.init_ui()
    
    def init_ui(self):
        QLabel("Ventana de Opciones", self).move(150, 50)
        # Implementación de la interfaz de usuario para las opciones
        b_Tareas_Pendientes = QPushButton("Ver Tareas Pendientes", self)
        b_Tareas_Pendientes.move(150, 50)
        #b_Tareas_Pendientes.clicked.connect(self.open_pending_tasks)
        #self.setCentralWidget(b_Tareas_Pendientes)
        b_Gestion_Usuarios = QPushButton("Gestión de Usuarios", self)
        b_Tareas_Diarias = QPushButton("Tareas Diarias", self)
        b_Ingresos = QPushButton("Ingresos", self)
'''
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt

from views.dashboard_view import MainWindow  # Ajusta la ruta según tu carpeta

class OptionsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú de Opciones - Sistema de Gestión")
        self.resize(400, 450) # Un poco más alta para que respire el diseño
        self.init_ui()
        
    def open_pending_tasks(self):
        # 1. Creamos la instancia de la ventana de tareas
        # La guardamos en self para que Python no la borre de la memoria (Garbage Collector)
        self.dashboard = MainWindow()
        
        # 2. Mostramos la nueva ventana
        self.dashboard.show()
        
        # 3. Cerramos (o minimizamos) la ventana actual de opciones
        self.close()
    
    def init_ui(self):
        # 1. Creamos un Widget Central (obligatorio en QMainWindow)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 2. Layout principal (Vertical)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 30, 50, 30) # Márgenes laterales para que no toquen los bordes
        layout.setSpacing(15) # Espacio entre cada botón

        # 3. Título estilizado
        label_titulo = QLabel("Panel Principal")
        # Estilo CSS simple para mejorar la apariencia
        label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        label_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_titulo)

        # 4. Línea separadora (Opcional, para orden visual)
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setFrameShadow(QFrame.Sunken)
        layout.addWidget(linea)

        # 5. Creación de botones
        # Los guardamos como atributos (self.) por si necesitas usarlos luego
        self.b_Tareas_Pendientes = QPushButton("Ver Tareas Pendientes")
        self.b_Tareas_Diarias = QPushButton("Tareas Diarias")
        self.b_Ingresos = QPushButton("Ingresos")
        self.b_Gestion_Usuarios = QPushButton("Gestión de Usuarios")
        
        # CONEXIÓN: Al hacer click, llama al método de arriba
        self.b_Tareas_Pendientes.clicked.connect(self.open_pending_tasks)
        
        # 6. Estilo para los botones (opcional pero recomendado)
        estilo_botones = """
            QPushButton {
                padding: 10px;
                font-size: 14px;
            }
        """
        for btn in [self.b_Tareas_Pendientes, self.b_Tareas_Diarias, 
                    self.b_Ingresos, self.b_Gestion_Usuarios]:
            btn.setStyleSheet(estilo_botones)
            layout.addWidget(btn)

        # 7. Espaciador al final para empujar todo hacia arriba
        layout.addStretch()