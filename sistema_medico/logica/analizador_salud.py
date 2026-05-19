import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class AnalizadorSalud:
    """Implementa análisis avanzado de datos de salud usando Pandas y Matplotlib."""
    
    def __init__(self, gestor):
        self._gestor = gestor
        self._df = None

    def _preparar_dataset(self):
        """Convierte los datos del gestor en un DataFrame de Pandas."""
        data = []
        for paciente in self._gestor.obtener_todos_los_pacientes():
            for consulta in paciente.consultas:  # Uso de propiedad pública
                data.append({
                    "Paciente": paciente.nombre,
                    "Edad": paciente.edad,
                    "Genero": paciente.genero,
                    "Fecha": pd.to_datetime(consulta.fecha),
                    "Sintomas": consulta.sintomas.lower(),
                    "Diagnostico": consulta.diagnostico,
                    "Tratamiento": consulta.tratamiento
                })
        
        if not data:
            return None
        
        self._df = pd.DataFrame(data)
        return self._df

    def generar_reporte_enfermedades(self):
        """Reporte de las enfermedades (diagnósticos) más comunes."""
        df = self._preparar_dataset()
        if df is None: return "No hay datos suficientes para el reporte."
        
        reporte = df['Diagnostico'].value_counts()
        return reporte

    def pacientes_frecuentes(self):
        """Identifica pacientes con mayor número de consultas."""
        df = self._preparar_dataset()
        if df is None: return "No hay datos suficientes."
        
        return df['Paciente'].value_counts()

    def edad_promedio_por_diagnostico(self):
        """Calcula la edad promedio de pacientes según su diagnóstico."""
        df = self._preparar_dataset()
        if df is None: return "Sin datos."
        
        return df.groupby('Diagnostico')['Edad'].mean()

    def graficar_distribucion(self):
        """Crea gráficos de distribución de enfermedades por edad y género."""
        df = self._preparar_dataset()
        if df is None: return
        
        # Gráfico por Edad
        plt.figure(figsize=(10, 5))
        df.groupby('Diagnostico')['Edad'].mean().plot(kind='bar', color='skyblue')
        plt.title('Edad Promedio por Diagnóstico')
        plt.ylabel('Edad')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('distribucion_edad.png')
        plt.show()

        # Gráfico por Género
        plt.figure(figsize=(10, 5))
        pd.crosstab(df['Diagnostico'], df['Genero']).plot(kind='bar', stacked=True)
        plt.title('Distribución de Diagnósticos por Género')
        plt.ylabel('Cantidad')
        plt.tight_layout()
        plt.savefig('distribucion_genero.png')
        plt.show()

    def graficar_tendencia_temporal(self):
        """Tendencia de consultas en el tiempo."""
        df = self._preparar_dataset()
        if df is None: return
        
        df_sorted = df.sort_values('Fecha')
        df_sorted.set_index('Fecha', inplace=True)
        tendencia = df_sorted.resample('ME').size()  # Agrupar por mes

        plt.figure(figsize=(10, 5))
        tendencia.plot(marker='o', color='green')
        plt.title('Tendencia de Consultas Mensuales')
        plt.ylabel('Número de Consultas')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('tendencia_consultas.png')
        plt.show()

    def sugerir_chequeos_preventivos(self):
        """Analiza la frecuencia de síntomas para sugerir chequeos automáticos."""
        df = self._preparar_dataset()
        if df is None: return []
        
        recomendaciones = []
        mapeo_preventivo = {
            "tos": ("Chequeo Pulmonar", "Rayos X de Tórax", "🫁"),
            "dolor de cabeza": ("Examen Neurológico", "Presión Arterial", "🧠"),
            "fiebre": ("Análisis de Sangre", "Hemograma Completo", "🌡️"),
            "cansancio": ("Perfil Tiroideo", "Prueba de Anemia", "😴"),
            "dolor estomago": ("Gastroenterología", "Ecografía Abdominal", "🤢"),
            "sed": ("Prueba de Glucosa", "Diabetes / Glucemia", "🥤")
        }
        
        todos_sintomas = " ".join(df['Sintomas'].tolist())
        
        for sintoma, info in mapeo_preventivo.items():
            if sintoma in todos_sintomas:
                recomendaciones.append({
                    "sintoma": sintoma,
                    "titulo": info[0],
                    "detalle": info[1],
                    "icono": info[2],
                    "tipo": "PREVENTIVO"
                })
        
        return recomendaciones
