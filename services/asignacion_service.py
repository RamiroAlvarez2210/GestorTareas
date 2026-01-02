import requests,datetime

from models.task_data import Asignacion

class AsignacionService:
    #def __init__(self, base_url):
    #    self.base_url = base_url
        
        # Diccionarios para convertir códigos de API a texto legible
        #self.mapa_estados = {0: "Pendiente", 1: "En Progreso", 2: "Cerrado"}
        #self.mapa_prioridades = {0: "Baja", 1: "Media", 2: "Alta"}


    def asignar_tarea(self, tarea, usuario):
        # Lógica para asignar una tarea a un usuario
        pass

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
        
    def crear_asignacion(self, asignacion):
        '''try:
            payload = {
                "fecha": asignacion.fecha.isoformat(),
                "nombreUsuario": asignacion.usuario,
                "nombreEquipo": asignacion.equipo,
                "serial": asignacion.serial
            }
            response = requests.post(f"{self.base_url}/Asignacion", json=payload, timeout=5)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error al crear asignación en la API: {e}")
            return False'''
        try:
            # POST http://localhost:5240/api/tasks
            response = requests.post(f"{self.base_url}/Tarea", json=asignacion, timeout=5)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error al crear tarea: {e}")
            return False
