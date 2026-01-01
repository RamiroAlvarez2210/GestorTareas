import requests
from datetime import datetime
from models.task_data import Tarea,Asignacion

class TaskAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        
        # Diccionarios para convertir códigos de API a texto legible
        self.mapa_estados = {0: "Pendiente", 1: "En Progreso", 2: "Cerrado"}
        self.mapa_prioridades = {0: "Baja", 1: "Media", 2: "Alta"}

    def obtener_tareas(self):
        try:
            response = requests.get(f"{self.base_url}/Tarea", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            tareas_procesadas = []
            for item in data:
                # Usamos .get() con valores por defecto para evitar errores si falta una llave
                # y 'or' para manejar los valores que vienen como null (None)
                titulo = item.get('titulo') or "Sin Título"
                usuario = item.get('nombreUsuario') or "Sin Asignar"
                
                # Convertimos los números de la API a texto usando nuestros mapas
                estado_num = item.get('estado', 0)
                prioridad_num = item.get('prioridad', 0)
                
                estado_texto = self.mapa_estados.get(estado_num, "Desconocido")
                prioridad_texto = self.mapa_prioridades.get(prioridad_num, "Baja")

                t = Tarea(
                    ticket=item.get('ticket', 0), # Asumimos ID 0 si no viene
                    titulo=titulo,
                    estado=estado_texto,
                    prioridad=prioridad_texto,
                    usuario_solicitante=usuario,
                    # Manejo de fecha: si no viene, usamos la actual
                    ultima_actualizacion=datetime.now(), 
                    descripcion=item.get('descripcion', "") or "",
                    movimientos=[]
                )
                tareas_procesadas.append(t)
            return tareas_procesadas
        except Exception as e:
            print(f"Error al obtener tareas de la API: {e}")
            return []
        
    def obtener_asignaciones(self):
        try:
            response = requests.get(f"{self.base_url}/Asignacion", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            asignaciones = []
            for item in data:
                # Procesar fecha (asumiendo formato ISO string desde la API)
                fecha_str = item.get('fecha')
                fecha_dt = datetime.now()
                if fecha_str:
                    try:
                        fecha_dt = datetime.fromisoformat(fecha_str)
                    except ValueError:
                        pass
                
                asignacion = Asignacion(
                    fecha=fecha_dt,
                    usuario=item.get('nombreUsuario') or "Sin Asignar",
                    equipo=item.get('nombreEquipo') or "Sin Equipo",
                    serial=item.get('serial') or "S/N"
                )
                asignaciones.append(asignacion)
            return asignaciones
        except Exception as e:
            print(f"Error al obtener asignaciones de la API: {e}")
            return []

    def crear_tarea(self, datos):
        try:
            # POST http://localhost:5240/api/tasks
            response = requests.post(f"{self.base_url}/Tarea", json=datos, timeout=5)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error al crear tarea: {e}")
            return False