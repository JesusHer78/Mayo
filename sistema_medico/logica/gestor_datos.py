import json
import os
from ..clases.paciente import Paciente
from ..clases.consulta import Consulta

class GestorDatos:
    """
    Clase encargada de la persistencia de datos y la gestión central de pacientes.
    Actúa como un controlador que conecta los datos almacenados con la lógica del negocio.
    """
    
    def __init__(self, archivo="sistema_medico/datos/datos_pacientes.json"):
        """
        Constructor que inicializa el gestor y carga datos existentes.
        :param archivo: Ruta al archivo JSON de persistencia.
        """
        self._pacientes = []
        self._archivo = archivo
        # Asegura que el directorio exista (Buenas prácticas de gestión de archivos)
        os.makedirs(os.path.dirname(self._archivo), exist_ok=True)
        self.cargar_datos()

    def registrar_paciente(self, paciente):
        """Añade un objeto Paciente a la lista en memoria."""
        self._pacientes.append(paciente)

    def buscar_paciente_por_nombre(self, nombre):
        """Busca un paciente por coincidencia exacta de nombre."""
        for p in self._pacientes:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def buscar_avanzado(self, query, modo="Nombre"):
        """
        Realiza búsquedas filtradas según diferentes criterios.
        :param query: Texto o valor a buscar.
        :param modo: Criterio de búsqueda ('Nombre', 'Edad', 'Diagnóstico').
        :return: Lista de pacientes que cumplen el criterio.
        """
        query = str(query).lower()
        resultados = []
        for p in self._pacientes:
            if modo == "Nombre" and query in p.nombre.lower(): 
                resultados.append(p)
            elif modo == "Edad" and query == str(p.edad): 
                resultados.append(p)
            elif modo == "Diagnóstico":
                # Busca en todas las consultas del paciente para ver si tuvo ese diagnóstico
                for c in p.consultas:
                    if query in c.diagnostico.lower():
                        resultados.append(p)
                        break
        return resultados

    def obtener_todos_los_pacientes(self):
        """Retorna la lista completa de pacientes registrados."""
        return self._pacientes

    def guardar_datos(self):
        """
        Serializa los objetos de Python a un formato JSON para persistencia.
        Convierte objetos complejos en diccionarios anidados.
        """
        datos = []
        for p in self._pacientes:
            p_dict = {
                "nombre": p.nombre, "edad": p.edad, "genero": p.genero,
                "historial": p.historial_medico, "consultas": []
            }
            # Mapeo de objetos Consulta a diccionarios
            for c in p.consultas:
                p_dict["consultas"].append({
                    "fecha": c.fecha, "sintomas": c.sintomas,
                    "diagnostico": c.diagnostico, "tratamiento": c.tratamiento
                })
            datos.append(p_dict)
            
        with open(self._archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_datos(self):
        """
        Lee el archivo JSON y reconstruye los objetos Paciente y Consulta (Deserialización).
        """
        if not os.path.exists(self._archivo): 
            return
            
        try:
            with open(self._archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            for d in datos:
                # Reconstrucción de la instancia Paciente
                p = Paciente(d["nombre"], d["edad"], d["genero"], d["historial"])
                # Reconstrucción de sus Consultas
                for c_data in d["consultas"]:
                    c = Consulta(c_data["fecha"], c_data["sintomas"], c_data["diagnostico"], c_data["tratamiento"])
                    p.agregar_consulta(c)
                self._pacientes.append(p)
        except Exception as e:
            print(f"⚠️ Error al cargar la base de datos: {e}")
