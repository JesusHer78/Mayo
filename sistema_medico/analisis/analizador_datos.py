import pandas as pd
import matplotlib.pyplot as plt
from ..ml.ia_preventiva import ModeloPreventivo

class AnalizadorDatos:
    """
    Clase especializada en el análisis estadístico y procesamiento de datos médicos.
    Hace uso intensivo de la librería Pandas para el manejo de estructuras de datos.
    """
    
    def __init__(self, gestor):
        """
        Inicializa el analizador vinculándolo a un gestor de datos.
        :param gestor: Instancia de GestorDatos que provee la información.
        """
        self._gestor = gestor
        self._ia = ModeloPreventivo() # Implementación de Machine Learning/IA

    def _preparar_dataset(self):
        """
        Método interno que transforma los objetos de la aplicación en un DataFrame de Pandas.
        Permite realizar operaciones vectorizadas y estadísticas de alto nivel.
        :return: pd.DataFrame organizado o None si la base está vacía.
        """
        data = []
        # Aplanamiento de la estructura de datos (Denormalización para análisis)
        for paciente in self._gestor.obtener_todos_los_pacientes():
            for consulta in paciente.consultas:
                data.append({
                    "Paciente": paciente.nombre,
                    "Edad": paciente.edad,
                    "Genero": paciente.genero,
                    "Fecha": pd.to_datetime(consulta.fecha),
                    "Sintomas": consulta.sintomas.lower(),
                    "Diagnostico": consulta.diagnostico,
                    "Tratamiento": consulta.tratamiento
                })
        return pd.DataFrame(data) if data else None

    def obtener_enfermedades_comunes(self):
        """Calcula la frecuencia de cada diagnóstico registrado."""
        df = self._preparar_dataset()
        return df['Diagnostico'].value_counts() if df is not None else "Sin datos"

    def obtener_pacientes_frecuentes(self):
        """Identifica a los pacientes con mayor cantidad de visitas al consultorio."""
        df = self._preparar_dataset()
        return df['Paciente'].value_counts() if df is not None else "Sin datos"

    def obtener_edad_promedio_diagnostico(self):
        """Calcula el promedio de edad agrupado por patología/enfermedad."""
        df = self._preparar_dataset()
        if df is not None:
            # Uso de groupby y agregación estadística
            return df.groupby('Diagnostico')['Edad'].mean()
        return None

    def obtener_sugerencias_ia(self):
        """
        Invoca al módulo de Machine Learning para analizar tendencias de síntomas
        y proponer chequeos médicos preventivos.
        """
        df = self._preparar_dataset()
        if df is not None:
            # Delegación de responsabilidad al módulo ML
            return self._ia.analizar_sintomas(df['Sintomas'])
        return "No hay suficientes datos para ejecutar el análisis de IA."
