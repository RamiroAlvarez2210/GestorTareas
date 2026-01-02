from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QDateEdit, QPushButton, QGroupBox, 
                             QFormLayout, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QDialog, QMessageBox, QCheckBox, QSpinBox)
from PyQt5.QtCore import QDate, Qt

from models.task_data import Asignacion
from services.api_service import TaskAPIClient # cambiar para generalizar api

# --- Sub-ventana de Impresión ---
class DialogoImpresion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Opciones de Impresión")
        self.setFixedSize(300, 200)
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.chk_software = QCheckBox("Carta de Software Legal")
        self.chk_software.setChecked(True)
        self.chk_remito = QCheckBox("Remitos")
        self.chk_remito.setChecked(True)

        layout.addWidget(QLabel("Seleccione documentos:"))
        layout.addWidget(self.chk_software)
        layout.addWidget(self.chk_remito)

        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Copias:"))
        self.spin_copias = QSpinBox()
        self.spin_copias.setRange(1, 10)
        h_layout.addWidget(self.spin_copias)
        layout.addLayout(h_layout)

        btn_confirmar = QPushButton("Imprimir ahora")
        btn_confirmar.clicked.connect(self.accept)
        layout.addWidget(btn_confirmar)

    def obtener_opciones(self):
        return {
            "software": self.chk_software.isChecked(),
            "remitos": self.chk_remito.isChecked(),
            "copias": self.spin_copias.value()
        }

# --- Vista Principal de Ingresos / Asignaciones ---
class IngresosWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api = TaskAPIClient("http://localhost:5240/api")
        self.tasks = []
        self.init_ui()
        self.refresh_data()


    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # --- FORMULARIO DE CARGA ---
        grupo_form = QGroupBox("Nueva Asignación de Equipo")
        form_layout = QHBoxLayout(grupo_form)
        
        col1 = QFormLayout()
        self.txt_usuario = QLineEdit() # Cambiado de Persona a Usuario
        self.txt_usuario.setPlaceholderText("Nombre del usuario receptor")
        self.fecha_asignacion = QDateEdit(calendarPopup=True)
        self.fecha_asignacion.setDate(QDate.currentDate())
        col1.addRow("Usuario:", self.txt_usuario)
        col1.addRow("Fecha:", self.fecha_asignacion)
        
        col2 = QFormLayout()
        self.txt_marca = QLineEdit()
        self.txt_modelo = QLineEdit()
        self.txt_serial = QLineEdit()
        col2.addRow("Marca:", self.txt_marca)
        col2.addRow("Modelo:", self.txt_modelo)
        col2.addRow("Serial:", self.txt_serial)
        
        self.btn_guardar = QPushButton("💾 Guardar\nAsignación")
        self.btn_guardar.setFixedSize(110, 80)
        self.btn_guardar.clicked.connect(self.ejecutar_guardado)

        form_layout.addLayout(col1, 2)
        form_layout.addLayout(col2, 2)
        form_layout.addWidget(self.btn_guardar)
        layout.addWidget(grupo_form)

        # --- CABECERA DE HISTORIAL CON FILTRO ---
        header_historial = QHBoxLayout()
        header_historial.addWidget(QLabel("<b>📜 Historial de Asignaciones</b>"))
        
        header_historial.addStretch() # Empuja el buscador a la derecha
        
        header_historial.addWidget(QLabel("🔍 Filtrar por Serial:"))
        self.txt_filtro_serial = QLineEdit()
        self.txt_filtro_serial.setPlaceholderText("Escriba el serial...")
        self.txt_filtro_serial.setFixedWidth(200)
        # Conectamos el evento de escribir con la función de filtrado
        self.txt_filtro_serial.textChanged.connect(self.filtrar_tabla)
        header_historial.addWidget(self.txt_filtro_serial)
        
        layout.addLayout(header_historial)

        

        # --- TABLA DE HISTORIAL ---
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(5)
        self.tabla_historial.setHorizontalHeaderLabels(["Fecha", "Usuario", "Equipo", "Serial", "Acción"])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_historial.verticalHeader().setVisible(False)
        layout.addWidget(self.tabla_historial)

        # Cargar algunos datos para probar el buscador
        #self.cargar_datos_ejemplo()

    def refresh_data(self):
            """Llama a la API y refresca la tabla"""
            # En una app real, esto debería ir en un QThread para no congelar la UI
            self.tasks = self.api.obtener_asignaciones()
            self.load_data()    

    def load_data(self):
        self.tabla_historial.setRowCount(0)
        for row, task in enumerate(self.tasks):
            self.tabla_historial.insertRow(row)
            fecha_str = task.fecha.strftime("%Y-%m-%d") if hasattr(task.fecha, "strftime") else str(task.fecha)
            self.tabla_historial.setItem(row, 0, QTableWidgetItem(fecha_str))
            self.tabla_historial.setItem(row, 1, QTableWidgetItem(task.usuario))
            
            # Accedemos a los datos dentro del objeto Equipo
            descripcion_equipo = f"{task.equipo.marca} {task.equipo.modelo}".strip()
            if not descripcion_equipo: descripcion_equipo = task.equipo.nombre
                
            self.tabla_historial.setItem(row, 2, QTableWidgetItem(descripcion_equipo))
            self.tabla_historial.setItem(row, 3, QTableWidgetItem(task.equipo.serial))
            
            btn = QPushButton("🖨️ Reimprimir")
            btn.clicked.connect(lambda ch, r=row: self.reimprimir_desde_tabla(r))
            self.tabla_historial.setCellWidget(row, 4, btn)

    def cargar_datos_ejemplo(self):
        # Datos de prueba para verificar el filtro por serial
        datos = [
            ("2023-10-25", "Ricardo A.", "Dell Latitude", "SN999-ABC"),
            ("2023-10-24", "Maria G.", "HP ProBook", "SN888-XYZ"),
            ("2023-10-23", "Esteban Q.", "Lenovo T14", "SN777-LMN"),
        ]
        self.tabla_historial.setRowCount(len(datos))
        for i, (f, u, e, s) in enumerate(datos):
            self.tabla_historial.setItem(i, 0, QTableWidgetItem(f))
            self.tabla_historial.setItem(i, 1, QTableWidgetItem(u))
            self.tabla_historial.setItem(i, 2, QTableWidgetItem(e))
            self.tabla_historial.setItem(i, 3, QTableWidgetItem(s))
            
            btn = QPushButton("🖨️ Reimprimir")
            btn.clicked.connect(lambda ch, r=i: self.reimprimir_desde_tabla(r))
            self.tabla_historial.setCellWidget(i, 4, btn)

    def filtrar_tabla(self):
        """Filtra la tabla en tiempo real comparando con la columna 'Serial' (índice 3)"""
        texto_busqueda = self.txt_filtro_serial.text().lower()
        for i in range(self.tabla_historial.rowCount()):
            item_serial = self.tabla_historial.item(i, 3)
            if item_serial:
                # Si el texto de búsqueda está en el serial, mostramos la fila, sino la ocultamos
                mostrar = texto_busqueda in item_serial.text().lower()
                self.tabla_historial.setRowHidden(i, not mostrar)

    def ejecutar_guardado(self):
        if not self.txt_usuario.text() or not self.txt_serial.text():
            QMessageBox.warning(self, "Atención", "Usuario y Serial son obligatorios")
            return

        # Simulación de guardado
        # Convertimos a diccionario y formateamos la fecha a string para evitar errores de serialización JSON
        datos_asignacion = {
            "fecha": self.fecha_asignacion.date().toPyDate().isoformat(),
            "usuario": self.txt_usuario.text(),
            "marca": self.txt_marca.text(),
            "modelo": self.txt_modelo.text(),
            "serial": self.txt_serial.text()
        }
        exito = self.api.crear_asignacion(datos_asignacion)

        if exito:
            QMessageBox.information(self, "Éxito", "La asignación se guardó correctamente.")
            self.refresh_data() # Recargar la tabla desde la API
        else:
            QMessageBox.critical(self, "Error", "Hubo un problema al guardar la asignación.")
            return
        # Preguntar si desea imprimir documentos
        respuesta = QMessageBox.question(
            self, "Impresión", "¿Desea imprimir los documentos?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            diag = DialogoImpresion(self)
            diag.exec_()
        
        self.limpiar_formulario()

    def reimprimir_desde_tabla(self, fila):
        serial = self.tabla_historial.item(fila, 3).text()
        QMessageBox.information(self, "Reimpresión", f"Reimprimiendo documentos para equipo serial: {serial}")

    def limpiar_formulario(self):
        self.txt_usuario.clear()
        self.txt_marca.clear()
        self.txt_modelo.clear()
        self.txt_serial.clear()
        self.fecha_asignacion.setDate(QDate.currentDate())