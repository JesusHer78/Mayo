import sys
import os

# Agregamos el directorio raíz del proyecto al path de búsqueda de módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.paciente import Paciente
from clases.consulta import Consulta
from logica.gestor_consultorio import GestorConsultorio
from logica.analizador_salud import AnalizadorSalud

def menu_analisis(gestor):
    """Submenú para el análisis de salud."""
    analizador = AnalizadorSalud(gestor)
    
    while True:
        print("\n--- MÓDULO DE ANÁLISIS DE SALUD (PANDAS/MATPLOTLIB) ---")
        print("1. Reporte de Enfermedades Comunes")
        print("2. Pacientes Frecuentes")
        print("3. Edad Promedio por Diagnóstico")
        print("4. Generar Gráficos de Distribución (Edad/Género)")
        print("5. Generar Gráfico de Tendencia Temporal")
        print("6. Análisis de Chequeos Preventivos (Innovador)")
        print("7. Volver al menú principal")
        
        opc = input("Seleccione una opción: ")
        
        if opc == "1":
            print("\nReporte de Diagnósticos:")
            print(analizador.generar_reporte_enfermedades())
        elif opc == "2":
            print("\nPacientes con más consultas:")
            print(analizador.pacientes_frecuentes())
        elif opc == "3":
            print("\nEdad promedio por diagnóstico:")
            print(analizador.edad_promedio_por_diagnostico())
        elif opc == "4":
            print("\nGenerando gráficos de distribución...")
            analizador.graficar_distribucion()
        elif opc == "5":
            print("\nGenerando gráfico de tendencia...")
            analizador.graficar_tendencia_temporal()
        elif opc == "6":
            print("\nAnalizando síntomas...")
            print(analizador.sugerir_chequeos_preventivos())
        elif opc == "7":
            break
        else:
            print("Opción no válida.")

def menu_principal():
    """Menú interactivo del sistema."""
    gestor = GestorConsultorio()
    
    while True:
        print("\n--- SISTEMA AVANZADO DE CONSULTORIO MÉDICO ---")
        print("1. Registrar Paciente")
        print("2. Registrar Consulta")
        print("3. Ver Historial de Paciente")
        print("4. Listar Todos los Pacientes")
        print("5. MÓDULO DE ANÁLISIS DE SALUD")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del paciente: ")
            edad = int(input("Edad: "))
            genero = input("Género: ")
            historial = input("Historial médico previo: ")
            p = Paciente(nombre, edad, genero, historial)
            gestor.registrar_paciente(p)
            print(f"Paciente '{nombre}' registrado con éxito.")
            
        elif opcion == "2":
            nombre = input("Nombre del paciente a consultar: ")
            p = gestor.buscar_paciente_por_nombre(nombre)
            if p:
                fecha = input("Fecha de la consulta (YYYY-MM-DD): ")
                sintomas = input("Síntomas: ")
                diagnostico = input("Diagnóstico: ")
                tratamiento = input("Tratamiento indicado: ")
                c = Consulta(fecha, sintomas, diagnostico, tratamiento)
                p.agregar_consulta(c)
                print("Consulta guardada satisfactoriamente.")
            else:
                print("Error: Paciente no encontrado.")
                
        elif opcion == "3":
            nombre = input("Nombre del paciente: ")
            p = gestor.buscar_paciente_por_nombre(nombre)
            if p:
                print(p.mostrar_historial_completo())
            else:
                print("Error: Paciente no encontrado.")
                
        elif opcion == "4":
            pacientes = gestor.obtener_todos_los_pacientes()
            if not pacientes:
                print("Aún no hay pacientes registrados.")
            else:
                print("\nLISTADO DE PACIENTES:")
                for p in pacientes:
                    print("-" * 20)
                    print(p.mostrar_info())
                    
        elif opcion == "5":
            menu_analisis(gestor)
            
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()
