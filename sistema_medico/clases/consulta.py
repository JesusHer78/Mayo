class Consulta:
    """
    Clase que representa una visita o consulta médica individual.
    Almacena los datos cruciales de una atención clínica para su posterior análisis.
    """
    
    def __init__(self, fecha, sintomas, diagnostico, tratamiento):
        """
        Constructor de Consulta.
        :param fecha: Fecha en formato string (YYYY-MM-DD).
        :param sintomas: Descripción de las molestias del paciente.
        :param diagnostico: Conclusión médica tras la evaluación.
        :param tratamiento: Medicamentos o pasos a seguir indicados.
        """
        self._fecha = fecha
        self._sintomas = sintomas
        self._diagnostico = diagnostico
        self._tratamiento = tratamiento

    @property
    def fecha(self):
        """Retorna la fecha de la consulta."""
        return self._fecha

    @property
    def sintomas(self):
        """Retorna los síntomas registrados."""
        return self._sintomas

    @property
    def diagnostico(self):
        """Retorna el diagnóstico emitido."""
        return self._diagnostico

    @property
    def tratamiento(self):
        """Retorna el tratamiento prescrito."""
        return self._tratamiento

    def mostrar_detalles(self):
        """
        Formatea los detalles de la consulta en una cadena legible para el usuario.
        """
        return (f"📅 Fecha        : {self._fecha}\n"
                f"🌡️ Síntomas     : {self._sintomas}\n"
                f"🩺 Diagnóstico : {self._diagnostico}\n"
                f"💊 Tratamiento : {self._tratamiento}\n")
