import sys
import os

# Agregamos el directorio raíz del proyecto al path de búsqueda de módulos
sys.path.append(r"c:\Users\uzuma\Desktop\clientemayo\sistema_medico")

from clases.paciente import Paciente
from clases.consulta import Consulta
from logica.gestor_consultorio import GestorConsultorio

def test_system():
    # Inicializar el gestor
    gestor = GestorConsultorio()
    
    # Registrar un paciente
    p1 = Paciente("Juan Perez", 30, "Masculino", "Ninguno")
    gestor.registrar_paciente(p1)
    
    # Crear una consulta
    c1 = Consulta("2025-05-10", "Dolor de cabeza", "Migraña", "Paracetamol")
    p1.agregar_consulta(c1)
    
    # Verificar información básica
    print("Prueba de mostrar_info (Polimorfismo):")
    print(p1.mostrar_info())
    
    # Verificar historial completo
    print("\nPrueba de historial completo:")
    print(p1.mostrar_historial_completo())
    
    # Probar búsqueda
    print("\nBuscando a Juan Perez...")
    res = gestor.buscar_paciente_por_nombre("Juan Perez")
    if res:
        print(f"Paciente encontrado: {res.nombre}")
    else:
        print("ERROR: Paciente no encontrado.")

if __name__ == "__main__":
    test_system()
