import requests
from datetime import datetime
from models.task_data import Tarea, Asignacion, Equipo

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
                    public_id=item.get('publicId'),
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
                
                # --- RESOLUCIÓN DE USUARIO ---
                usuario_id = item.get('usuarioId')
                nombre_usuario = "Sin Asignar"
                
                if usuario_id:
                    try:
                        # Consultamos la API de Usuarios para obtener el nombre real
                        resp_usr = requests.get(f"{self.base_url}/Usuario/{usuario_id}", timeout=5)
                        if resp_usr.status_code == 200:
                            data_usr = resp_usr.json()
                            nombre_usuario = data_usr.get('nombre') or data_usr.get('nombreUsuario') or usuario_id
                        else:
                            nombre_usuario = usuario_id # Si falla, mostramos el ID
                    except Exception:
                        nombre_usuario = usuario_id

                # --- RESOLUCIÓN DE EQUIPO ---
                equipo_id = item.get('equipoId')
                
                nombre_eq = "Sin Equipo"
                marca_eq = ""
                modelo_eq = ""
                serial_eq = "S/N"
                
                if equipo_id:
                    try:
                        # Buscamos el detalle del equipo: serial, marca, modelo
                        resp_eq = requests.get(f"{self.base_url}/Equipo/{equipo_id}", timeout=5)
                        if resp_eq.status_code == 200:
                            data_eq = resp_eq.json()
                            marca_eq = data_eq.get('marca', '')
                            modelo_eq = data_eq.get('modelo', '')
                            serial_eq = data_eq.get('serial', serial_eq)
                            nombre_eq = data_eq.get('nombre') or f"{marca_eq} {modelo_eq}".strip()
                    except Exception:
                        pass 

                # Creamos el objeto Equipo
                equipo_obj = Equipo(nombre=nombre_eq, marca=marca_eq, modelo=modelo_eq, serial=serial_eq)

                asignacion = Asignacion(
                    public_id=item.get('publicId'),
                    fecha=fecha_dt,
                    usuario=nombre_usuario,
                    equipo=equipo_obj
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
        
    def crear_asignacion(self, datos):
        try:
            # Mapeamos los datos del diccionario a la estructura que pide la API
            payload = {
                "nombreUsuario": datos.get("usuario"),
                "marcaEquipo": datos.get("marca"),
                "modeloEquipo": datos.get("modelo"),
                "serialEquipo": datos.get("serial"),
                "fecha": datos.get("fecha")
            }
            response = requests.post(f"{self.base_url}/Asignacion/AltaUsuarioEquipo", json=payload, timeout=5)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error al crear asignación: {e}")
            return False
