from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QLabel, QHBoxLayout, QComboBox,
                             QDialog)
from PyQt5.QtCore import Qt, QEvent
from views.detail_view import TaskDetailWindow
from models.task_data import get_mock_data, crear_tarea_vacia

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Tareas")
        self.resize(900, 600)
        self.tasks = get_mock_data()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # ... (Mantener Toolbar igual) ...
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("<b>Listado de Tareas Pendientes</b>"))
        top_bar.addStretch()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Prioridad (Mayor a Menor)", "Fecha Actualización", "Estado"])
        top_bar.addWidget(self.sort_combo)
        layout.addLayout(top_bar)

        # Configuración de la Tabla
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        columns = ["ID", "Título", "Estado", "Prioridad", "Solicitante", "Última Actualización"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # --- SOLUCIÓN: INSTALAR FILTRO DE EVENTOS ---
        # Esto permite que la ventana capture los clics que ocurren DENTRO de la tabla
        self.table.viewport().installEventFilter(self)

        layout.addWidget(self.table)
        self.load_data()

    def eventFilter(self, source, event):
        # Verificamos si el evento es un doble clic en el área de contenido de la tabla
        if source is self.table.viewport() and event.type() == QEvent.MouseButtonDblClick:
            # itemAt busca si hay una celda en las coordenadas donde hiciste clic
            item = self.table.itemAt(event.pos())
            
            if item is not None:
                # Si hay un ítem, abrimos detalle normal
                self.open_task_detail()
            else:
                # Si NO hay ítem (clic en el espacio blanco de abajo), creamos nueva tarea
                self.crear_nueva_tarea_rapida()
            return True
        return super().eventFilter(source, event)

    def load_data(self):
        self.table.setRowCount(0)
        for row, task in enumerate(self.tasks):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(task.id)))
            self.table.setItem(row, 1, QTableWidgetItem(task.titulo))
            self.table.setItem(row, 2, QTableWidgetItem(task.estado))
            self.table.setItem(row, 3, QTableWidgetItem(task.prioridad))
            self.table.setItem(row, 4, QTableWidgetItem(task.usuario_solicitante))
            self.table.setItem(row, 5, QTableWidgetItem(task.ultima_actualizacion.strftime("%Y-%m-%d %H:%M")))

    def open_task_detail(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            task_id = int(self.table.item(current_row, 0).text())
            selected_task = next((t for t in self.tasks if t.id == task_id), None)
            if selected_task:
                detail_window = TaskDetailWindow(selected_task, self)
                detail_window.exec_()
                self.load_data()

    def crear_nueva_tarea_rapida(self):
        nueva_tarea = crear_tarea_vacia()
        detalle_nueva = TaskDetailWindow(nueva_tarea, self)
        detalle_nueva.setWindowTitle("Crear Nueva Tarea")
        
        if detalle_nueva.exec_() == QDialog.Accepted:
            # Lógica para autoincrementar ID y guardar
            nueva_tarea.id = max([t.id for t in self.tasks], default=0) + 1
            self.tasks.append(nueva_tarea)
            self.load_data()