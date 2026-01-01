# views/detail_view.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTabWidget, QWidget, QFormLayout, 
                             QLineEdit, QComboBox, QTextEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHBoxLayout, QMessageBox,
                             QHeaderView)
from PyQt5.QtCore import Qt
from datetime import datetime

class TaskDetailWindow(QDialog):
    def __init__(self, tarea, parent=None):
        super().__init__(parent)
        self.tarea = tarea
        self.setWindowTitle(f"Detalle de Tarea #{self.tarea.ticket}")
        self.resize(600, 500)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Sistema de Pestañas
        self.tabs = QTabWidget()
        self.tab_info = QWidget()
        self.tab_history = QWidget()
        
        self.tabs.addTab(self.tab_info, "Información General")
        self.tabs.addTab(self.tab_history, "Movimientos e Historial")
        
        self.setup_info_tab()
        self.setup_history_tab()
        
        main_layout.addWidget(self.tabs)
        
        # Botones de Acción Global
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Guardar Cambios")
        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(self.close)
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_close)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def setup_info_tab(self):
        layout = QFormLayout()
        
        self.txt_titulo = QLineEdit(self.tarea.titulo)
        self.txt_desc = QTextEdit(self.tarea.descripcion)

        self.txt_user = QLineEdit(self.tarea.usuario_solicitante) # Probar
        
        self.cmb_estado = QComboBox()
        self.cmb_estado.addItems(["Pendiente", "En Progreso", "Cerrado"])
        self.cmb_estado.setCurrentText(self.tarea.estado)
        
        self.cmb_prioridad = QComboBox()
        self.cmb_prioridad.addItems(["Alta", "Media", "Baja"])
        self.cmb_prioridad.setCurrentText(self.tarea.prioridad)

        layout.addRow("Título:", self.txt_titulo)
        layout.addRow("Estado:", self.cmb_estado)
        layout.addRow("Prioridad:", self.cmb_prioridad)
        layout.addRow("Solicitante:", self.txt_user) # QLabel(self.tarea.usuario_solicitante)) # Read-only
        layout.addRow("Descripción:", self.txt_desc)
        
        self.tab_info.setLayout(layout)

    def setup_history_tab(self):
        layout = QVBoxLayout()
        
        # Tabla de Movimientos
        self.table_movs = QTableWidget()
        self.table_movs.setColumnCount(3)
        self.table_movs.setHorizontalHeaderLabels(["Fecha", "Usuario", "Movimiento"])
        self.table_movs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # Ajusta columnas en la tabla
        #self.table_movs.verticalHeader().setVisible(False)
        self.load_movements()
        
        # Sección para agregar nuevo movimiento
        input_layout = QHBoxLayout()
        self.txt_new_mov = QLineEdit()
        self.txt_new_mov.setPlaceholderText("Ingresar nuevo movimiento...")
        btn_add_mov = QPushButton("Agregar")
        btn_add_mov.clicked.connect(self.add_movement)
        
        input_layout.addWidget(self.txt_new_mov)
        input_layout.addWidget(btn_add_mov)
        
        layout.addWidget(self.table_movs)
        layout.addLayout(input_layout)
        self.tab_history.setLayout(layout)

    def load_movements(self):
        self.table_movs.setRowCount(len(self.tarea.movimientos))
        for row, mov in enumerate(self.tarea.movimientos):
            self.table_movs.setItem(row, 0, QTableWidgetItem(mov.fecha))
            self.table_movs.setItem(row, 1, QTableWidgetItem(mov.usuario))
            self.table_movs.setItem(row, 2, QTableWidgetItem(mov.descripcion))

    def add_movement(self):
        texto = self.txt_new_mov.text()
        if texto:
            row = self.table_movs.rowCount()
            self.table_movs.insertRow(row)
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.table_movs.setItem(row, 0, QTableWidgetItem(now))
            self.table_movs.setItem(row, 1, QTableWidgetItem("Usuario Actual"))
            self.table_movs.setItem(row, 2, QTableWidgetItem(texto))
            self.txt_new_mov.clear()
    def guardar_cambios(self):
        # Recolectar datos de los campos de la interfaz
        datos_actualizados = {
            "titulo": self.txt_titulo.text(),
            "estado": self.cmb_estado.currentText(),
            "prioridad": self.cmb_prioridad.currentText(),
            "descripcion": self.txt_desc.toPlainText()
        }
        
        # Llamar a la API (puedes pasar el cliente API desde el padre)
        exito = self.parent().api.actualizar_tarea(self.tarea.id, datos_actualizados)
        
        if exito:
            self.accept() # Cierra y refresca
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar en el servidor")