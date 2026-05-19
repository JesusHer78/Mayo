import json
import os
try:
    from clases.paciente import Paciente
    from clases.consulta import Consulta
except ImportError:
    from ..clases.paciente import Paciente
    from ..clases.consulta import Consulta

# Ruta absoluta al archivo de datos, independiente del directorio de ejecución
_DEFAULT_ARCHIVO = os.path.join(
    os.path.dirname(__file__), '..', 'datos', 'datos_pacientes.json'
)

class GestorConsultorio:
    """Clase para manejar la lógica de gestión del consultorio médico."""
    def __init__(self, archivo=None):
        self._pacientes = []
        self._archivo = archivo if archivo else os.path.normpath(_DEFAULT_ARCHIVO)
        self.cargar_datos()

    def registrar_paciente(self, paciente):
        """Registra un nuevo paciente en la lista del consultorio."""
        self._pacientes.append(paciente)

    def buscar_paciente_por_nombre(self, nombre):
        """Busca y retorna un paciente dado su nombre completo."""
        for p in self._pacientes:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def buscar_avanzado(self, query, modo="Nombre"):
        """Realiza una búsqueda avanzada por nombre, edad o diagnóstico."""
        query = str(query).lower()
        resultados = []
        
        for p in self._pacientes:
            if modo == "Nombre" and query in p.nombre.lower():
                resultados.append(p)
            elif modo == "Edad" and query == str(p.edad):
                resultados.append(p)
            elif modo == "Diagnóstico":
                for c in p.consultas:
                    if query in c.diagnostico.lower():
                        resultados.append(p)
                        break
        return resultados

    def obtener_todos_los_pacientes(self):
        """Retorna la lista de todos los pacientes registrados."""
        return self._pacientes

    def guardar_datos(self):
        """Persiste la información en un archivo JSON."""
        datos = []
        for p in self._pacientes:
            paciente_dict = {
                "nombre": p.nombre,
                "edad": p.edad,
                "genero": p.genero,
                "historial": p.historial_medico,
                "consultas": []
            }
            for c in p.consultas:
                paciente_dict["consultas"].append({
                    "fecha": c.fecha,
                    "sintomas": c.sintomas,
                    "diagnostico": c.diagnostico,
                    "tratamiento": c.tratamiento
                })
            datos.append(paciente_dict)
            
        with open(self._archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_datos(self):
        """Carga la información desde el archivo JSON si existe."""
        if not os.path.exists(self._archivo):
            return
            
        try:
            with open(self._archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
            for d in datos:
                p = Paciente(d["nombre"], d["edad"], d["genero"], d["historial"])
                for c_data in d["consultas"]:
                    c = Consulta(c_data["fecha"], c_data["sintomas"], c_data["diagnostico"], c_data["tratamiento"])
                    p.agregar_consulta(c)
                self._pacientes.append(p)
        except Exception as e:
            print(f"Error cargando datos: {e}")
