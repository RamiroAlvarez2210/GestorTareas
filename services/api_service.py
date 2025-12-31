import requests
from datetime import datetime
from models.task_data import Tarea

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
                    id=item.get('id', 0), # Asumimos ID 0 si no viene
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