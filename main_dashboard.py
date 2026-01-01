from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QStackedWidget, QFrame, QLabel)
from PyQt5.QtCore import Qt
from views.dashboard_view import MainWindow as TasksWidget # Reutilizamos tu tabla
# Importar otras vistas cuando las tengas (Usuarios, Ingresos, etc.)

from views.ingresos_view import IngresosWidget

from views.task_creation_view import TaskCreationWindow


class MainSystemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Integral de Gestión")
        self.resize(1200, 700)
        self.init_ui()

    def init_ui(self):
        # Widget y Layout Principal (Horizontal)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0) # Sin bordes exteriores
        main_layout.setSpacing(0)

        # --- 1. SIDEBAR (Lateral Izquierdo) ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: none;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 15px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton#active {
                background-color: #3498db;
                font-weight: bold;
            }
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setAlignment(Qt.AlignTop)

        # Botones del Sidebar
        # Botones del Sidebar actualizados
        self.btn_tasks = QPushButton("📋 Tareas Pendientes")
        self.btn_users = QPushButton("👥 Gestión Usuarios")
        self.btn_daily = QPushButton("📅 Tareas Diarias")
        # Cambiado: Icono de caja/entrega para Asignaciones
        self.btn_asignaciones = QPushButton("📦 Asignaciones / Ingresos")
        self.btn_new_task = QPushButton("➕ NUEVA TAREA")
        
        sidebar_layout.addWidget(self.btn_tasks)
        sidebar_layout.addWidget(self.btn_users)
        sidebar_layout.addWidget(self.btn_daily)
        #sidebar_layout.addWidget(self.btn_money)
        sidebar_layout.addWidget(self.btn_asignaciones)
        sidebar_layout.addWidget(self.btn_new_task)
        
        
        main_layout.addWidget(self.sidebar)

        # --- 2. ÁREA DE CONTENIDO (Derecha) ---
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        # Inicializar las páginas
        self.setup_pages()

        # Conectar botones a la lógica de cambio
        self.btn_tasks.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.btn_users.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        self.btn_daily.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))
        #self.btn_money.clicked.connect(lambda: self.content_stack.setCurrentIndex(3))
        self.btn_asignaciones.clicked.connect(lambda: self.content_stack.setCurrentIndex(3))
        self.btn_new_task.clicked.connect(self.mostrar_creador_tareas)
        # ... añadir los demás

    def setup_pages(self):
        # Página 0: Tu tabla de tareas (reutilizando el código previo)
        # Nota: Ajusta MainWindow para que herede de QWidget si solo quieres la tabla
        self.page_tasks = TasksWidget() 
        self.content_stack.addWidget(self.page_tasks)

        # Página 1: Placeholder para Usuarios
        self.page_users = QLabel("Sección de Gestión de Usuarios (Pendiente)")
        self.page_users.setAlignment(Qt.AlignCenter)
        self.content_stack.addWidget(self.page_users)
        
        # Página 2: Placeholder para Tareas Diarias
        self.page_daily = QLabel("Sección de Tareas Diarias (Pendiente)")
        self.page_daily.setAlignment(Qt.AlignCenter)
        self.content_stack.addWidget(self.page_daily)

        # Página 3: Ingresos
        self.page_ingresos = IngresosWidget()
        self.content_stack.addWidget(self.page_ingresos)
        
        # Página 4: Placeholder para Asignaciones
        self.page_asignaciones = QLabel("Sección de Asignaciones (Pendiente)")
        self.page_asignaciones.setAlignment(Qt.AlignCenter)
        self.content_stack.addWidget(self.page_asignaciones)
    
    def mostrar_creador_tareas(self):
        ventana_crear = TaskCreationWindow(self)
        if ventana_crear.exec_() == TaskCreationWindow.Accepted:
            datos = ventana_crear.obtener_datos()
            
            # Enviar a la API mediante el cliente que ya tienes en MainWindow
            # Accedemos al widget de tareas que está en el stack
            dashboard_widget = self.content_stack.widget(0) 
            
            # Creamos el endpoint en el API Client o usamos uno genérico
            exito = dashboard_widget.api.crear_tarea(datos)
            
            if exito:
                dashboard_widget.refresh_data() # Refrescamos la tabla automáticamente

# Para ejecutar
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainSystemWindow()
    win.show()
    sys.exit(app.exec_())