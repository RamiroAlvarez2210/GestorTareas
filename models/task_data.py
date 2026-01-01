# models/task_data.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Movimiento:
    fecha: str
    usuario: str
    descripcion: str

@dataclass
class Tarea:
    ticket: int
    titulo: str
    estado: str
    prioridad: str
    usuario_solicitante: str
    ultima_actualizacion: datetime
    descripcion: str = ""
    movimientos: List[Movimiento] = field(default_factory=list)

@dataclass
class Asignacion:
    #ticket: int
    fecha: datetime
    usuario: str
    equipo: str
    serial: str


# Datos Mock (Falsos) para probar la interfaz
def get_mock_data():
    return [
        Tarea(1, "Error en Login", "Pendiente", "Alta", "Juan Perez", datetime(2023, 10, 25, 14, 30), "Error al ingresar", 
              [Movimiento("2023-10-25 14:30", "Juan Perez", "Ticket creado")]),
        Tarea(2, "Actualizar Logo", "En Progreso", "Media", "Maria Lopez", datetime(2023, 10, 26, 9, 00), "Cambiar logo footer", []),
        Tarea(3, "Backup DB", "Cerrado", "Baja", "Admin", datetime(2023, 10, 24, 18, 00), "Backup mensual", []),
    ]
def crear_tarea_vacia():
    return Tarea(
        ticket=0,  # ID temporal
        titulo="",
        estado="Pendiente",
        prioridad="Baja",
        usuario_solicitante="Usuario Actual",
        ultima_actualizacion=datetime.now(),
        descripcion="",
        movimientos=[]
    )