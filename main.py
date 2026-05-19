"""
ARCHIVO PRINCIPAL (ENTRY POINT)
-------------------------------
Este archivo es el punto de inicio de la aplicación BUAP Medicine.
Se encarga de inicializar la interfaz gráfica y lanzar el bucle principal de ejecución.
Uso: python main.py
"""

from sistema_medico.gui.interfaz import BUAPMedicineApp

def main():
    """
    Función de arranque del sistema.
    Crea la instancia de la aplicación (que a su vez inicializa las capas de lógica y datos).
    """
    app = BUAPMedicineApp()
    
    # Inicia el bucle de eventos de Tkinter
    app.mainloop()

if __name__ == "__main__":
    # Asegura que el script solo se ejecute si es llamado directamente
    main()
