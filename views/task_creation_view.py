from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QComboBox, QTextEdit, QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt

class TaskCreationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nueva Tarea")
        self.resize(450, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        titulo_seccion = QLabel("<b>Nueva Solicitud de Tarea</b>")
        titulo_seccion.setStyleSheet("font-size: 16px;")
        layout.addWidget(titulo_seccion)

        form = QFormLayout()
        
        # Selección de tipo de tarea (Para escalabilidad futura)
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["Tarea Pendiente Estándar", "Tarea Diaria", "Soporte Técnico"])
        
        self.txt_titulo = QLineEdit()
        self.txt_titulo.setPlaceholderText("Ej: Error en servidor de base de datos")
        
        self.cmb_prioridad = QComboBox()
        self.cmb_prioridad.addItems(["Baja", "Media", "Alta"])
        
        self.txt_descripcion = QTextEdit()
        self.txt_descripcion.setPlaceholderText("Detalle el requerimiento aquí...")
        
        form.addRow("Tipo de Tarea:", self.cmb_tipo)
        form.addRow("Título:", self.txt_titulo)
        form.addRow("Prioridad:", self.cmb_prioridad)
        form.addRow("Descripción:", self.txt_descripcion)
        
        layout.addLayout(form)

        # Botones de Acción
        btn_layout = QHBoxLayout()
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.btn_crear = QPushButton("Generar Tarea")
        self.btn_crear.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold;")
        self.btn_crear.clicked.connect(self.validar_y_aceptar)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancelar)
        btn_layout.addWidget(self.btn_crear)
        
        layout.addLayout(btn_layout)

    def validar_y_aceptar(self):
        if not self.txt_titulo.text().strip():
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "El título es obligatorio para generar la tarea.")
            return
        self.accept()

    def obtener_datos(self):
        """Retorna un diccionario con la info para enviar a la API"""
        return {
            "titulo": self.txt_titulo.text(),
            "prioridad": self.cmb_prioridad.currentIndex(), # Enviamos el número a la API (0,1,2)
            "estado": 0, # Siempre inicia en Pendiente (0)
            "descripcion": self.txt_descripcion.toPlainText(),
            "tipo": self.cmb_tipo.currentText()
        }