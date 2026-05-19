from .persona import Persona

class Paciente(Persona):
    """
    Clase que representa a un paciente del consultorio.
    Hereda de la clase Persona para reutilizar atributos básicos.
    Gestiona el historial médico previo y las consultas realizadas en el sistema.
    """
    
    def __init__(self, nombre, edad, genero, historial_medico=None):
        """
        Constructor de Paciente.
        :para historial_medico: Cadena de texto o lista con antecedentes clínicos.
        """
        super().__init__(nombre, edad, genero)  # Llamada al constructor de la clase base (Herencia)
        self._historial_medico = historial_medico if historial_medico else ""
        self._consultas_realizadas = []  # Lista que contendrá objetos de la clase Consulta

    @property
    def historial_medico(self):
        """Getter para obtener el historial clínico previo."""
        return self._historial_medico

    @property
    def consultas(self):
        """Getter para acceder a la lista de consultas registradas."""
        return self._consultas_realizadas

    @historial_medico.setter
    def historial_medico(self, value):
        """Permite actualizar la información del historial clínico."""
        self._historial_medico = value

    def agregar_consulta(self, consulta):
        """
        Vincula una nueva consulta al registro histórico de este paciente.
        :param consulta: Instancia de la clase Consulta.
        """
        self._consultas_realizadas.append(consulta)

    def mostrar_info(self):
        """
        Sobrescribe mostrar_info de Persona (Polimorfismo).
        Extiende la información básica con datos específicos del paciente.
        """
        info_base = super().mostrar_info()
        return (f"[Ficha Paciente] {info_base}\n"
                f"Historial Prev.: {self._historial_medico}\n"
                f"Consultas Realizadas: {len(self._consultas_realizadas)}")

    def mostrar_historial_completo(self):
        """
        Genera un reporte detallado y legible de todas las consultas médicas del paciente.
        Recorre la lista de consultas y concatena sus detalles.
        """
        if not self._consultas_realizadas:
            return "No existen consultas registradas para este paciente."
        
        resultado = f"--- HISTORIAL CLÍNICO DETALLADO: {self._nombre.upper()} ---\n"
        for i, con in enumerate(self._consultas_realizadas, 1):
            resultado += f"\nVISITA #{i}:\n{con.mostrar_detalles()}"
            resultado += "-" * 40 + "\n"
        return resultado
