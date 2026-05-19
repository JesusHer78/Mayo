import sys
import os

# Agregamos el directorio raíz del proyecto al path de búsqueda de módulos
sys.path.append(r"c:\Users\uzuma\Desktop\clientemayo\sistema_medico")

from clases.paciente import Paciente
from clases.consulta import Consulta
from logica.gestor_consultorio import GestorConsultorio
from logica.analizador_salud import AnalizadorSalud

def test_analisis():
    gestor = GestorConsultorio()
    
    # Mock data
    p1 = Paciente("Alice", 25, "F", "N/A")
    p1.agregar_consulta(Consulta("2024-01-10", "tos y fiebre", "Gripe", "Reposo"))
    p1.agregar_consulta(Consulta("2024-02-15", "tos persistente", "Bronquitis", "Jarabe"))
    
    p2 = Paciente("Bob", 45, "M", "N/A")
    p2.agregar_consulta(Consulta("2024-01-20", "dolor de cabeza", "Migraña", "Aspirina"))
    
    p3 = Paciente("Charlie", 30, "M", "N/A")
    p3.agregar_consulta(Consulta("2024-03-05", "fiebre alta", "Gripe", "Antitérmico"))
    
    gestor.registrar_paciente(p1)
    gestor.registrar_paciente(p2)
    gestor.registrar_paciente(p3)
    
    analizador = AnalizadorSalud(gestor)
    
    print("Reporte de enfermedades:")
    print(analizador.generar_reporte_enfermedades())
    
    print("\nEdad promedio por diagnóstico:")
    print(analizador.edad_promedio_por_diagnostico())
    
    print("\nAnálisis preventivo:")
    print(analizador.sugerir_chequeos_preventivos())
    
    # No graficamos en el test por si no hay pantalla, pero grabamos
    # analizador.graficar_distribucion() # Comentado para evitar bloqueo en terminal remota

if __name__ == "__main__":
    test_analisis()
