import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importaciones locales bajo la nueva estructura de carpetas
from ..clases.paciente import Paciente
from ..clases.consulta import Consulta
from ..logica.gestor_datos import GestorDatos
from ..analisis.analizador_datos import AnalizadorDatos

class BUAPMedicineApp(tk.Tk):
    """
    Clase principal de la interfaz gráfica de usuario.
    Controla la navegación entre vistas y la interacción con las capas de lógica y datos.
    Sigue el patrón de Diseño de Software para interfaces de escritorio.
    """
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("BUAP Medicine")
        self.geometry("1100x800")
        self.configure(bg="#f0f2f5")
        
        # Inyección de dependencias (Capas de Lógica y Datos)
        self.gestor = GestorDatos()
        self.analisis = AnalizadorDatos(self.gestor)
        
        # Inicialización de la arquitectura visual
        self._setup_layout()
        self._setup_navigation()
        self._setup_frames()
        self.mostrar_vista("dashboard")

    def _setup_layout(self):
        """Configura la estructura básica de división de la pantalla (Sidebar vs Contenido)."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Panel lateral (Barra de navegación)
        self.sidebar = tk.Frame(self, bg="#2c3e50", width=220)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Contenedor principal para las diferentes vistas
        self.main_container = tk.Frame(self, bg="#f0f2f5")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

    def _setup_navigation(self):
        """Crea los botones de acceso rápido en el menú lateral."""
        tk.Label(self.sidebar, text="🩺BUAP Medicine ", font=("Segoe UI", 16, "bold"),
                 bg="#2c3e50", fg="white", pady=30).pack()
        
        nav = [
            ("🏠 Dashboard", "dashboard"), 
            ("👤 Registro", "registro"), 
            ("📝 Consulta", "consulta"), 
            ("🔍 Búsqueda", "busqueda"), 
            ("📊 Análisis", "analisis")
        ]
        # Generación dinámica de botones de menú
        for text, key in nav:
            tk.Button(self.sidebar, text=text, font=("Segoe UI", 11), bg="#2c3e50", fg="white", 
                      relief="flat", anchor="w", padx=20, command=lambda k=key: self.mostrar_vista(k)).pack(fill="x", pady=2)

    def _setup_frames(self):
        """Inicializa los contenedores (frames) para cada una de las secciones de la app."""
        self.frames = {}
        for key in ("dashboard", "registro", "consulta", "busqueda", "analisis"):
            f = tk.Frame(self.main_container, bg="#f0f2f5")
            self.frames[key] = f
            f.grid(row=0, column=0, sticky="nsew")
            # Carga los widgets específicos de cada sección
            self._crear_componentes(key, f)

    def mostrar_vista(self, name):
        """Eleva el frame solicitado al frente para hacerlo visible."""
        self.frames[name].tkraise()
        if name == "dashboard": self._actualizar_dashboard()

    def _crear_componentes(self, key, master):
        """Fábrica deUI que direcciona la creación de widgets según la sección."""
        if key == "dashboard": self._ui_dashboard(master)
        elif key == "registro": self._ui_registro(master)
        elif key == "consulta": self._ui_consulta(master)
        elif key == "busqueda": self._ui_busqueda(master)
        elif key == "analisis": self._ui_analisis(master)

    # --- COMPONENTES DE INTERFAZ (UI) ---
    
    def _ui_dashboard(self, m):
        """Crea la vista de resumen con tarjetas informativas y gráficos rápidos."""
        c = tk.Frame(m, bg="#f0f2f5", padx=30, pady=30)
        c.pack(fill="both", expand=True)
        tk.Label(c, text="Resumen de Operaciones", font=("Segoe UI", 20, "bold"), bg="#f0f2f5").pack(anchor="w")
        
        cards = tk.Frame(c, bg="#f0f2f5")
        cards.pack(fill="x", pady=20)
        self.lbl_p = self._card(cards, "Pacientes Totales", 0)
        self.lbl_c = self._card(cards, "Consultas Registradas", 1)
        
        self.plot_dash = tk.Frame(c, bg="white", height=350)
        self.plot_dash.pack(fill="both", expand=True)

    def _card(self, p, t, col):
        """Widget personalizado para mostrar indicadores clave (KPIs)."""
        f = tk.Frame(p, bg="white", padx=20, pady=20, relief="solid", borderwidth=1)
        f.grid(row=0, column=col, padx=10, sticky="nsew")
        p.grid_columnconfigure(col, weight=1)
        tk.Label(f, text=t, bg="white", fg="#3498db").pack(anchor="w")
        v = tk.Label(f, text="0", font=("Segoe UI", 24, "bold"), bg="white")
        v.pack(anchor="w")
        return v

    def _ui_registro(self, m):
        """Formulario centralizado para dar de alta nuevos pacientes."""
        f = tk.Frame(m, bg="white", padx=40, pady=40, relief="groove", borderwidth=1)
        f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(f, text="Formulario de Registro", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=(0,20))
        
        self.reg_n = self._input(f, "Nombre Completo:")
        self.reg_e = self._input(f, "Edad:")
        self.reg_g = tk.StringVar(value="Masculino")
        ttk.OptionMenu(f, self.reg_g, "Masculino", "Masculino", "Femenino").pack(fill="x", pady=5)
        self.reg_h = tk.Text(f, height=4, width=35) # Historial médico preliminar
        self.reg_h.pack(pady=5)
        
        tk.Button(f, text="GUARDAR PACIENTE", bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), 
                  command=self._h_reg).pack(fill="x", pady=(10, 5))
        
        tk.Button(f, text="LIMPIAR CAMPOS", bg="#95a5a6", fg="white", 
                  command=self._limpiar_reg).pack(fill="x", pady=5)

    def _input(self, p, t):
        """Helper para crear campos de entrada etiquetados."""
        tk.Label(p, text=t, bg="white").pack(anchor="w")
        e = tk.Entry(p, width=40)
        e.pack(pady=5)
        return e

    def _ui_consulta(self, m):
        """Vista para generar nuevas fichas de consulta médica."""
        f = tk.Frame(m, bg="white", padx=40, pady=40, relief="groove", borderwidth=1)
        f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(f, text="Registrar Nueva Atención", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=(0,20))
        
        self.con_pac_var = tk.StringVar()
        self.con_cb = ttk.OptionMenu(f, self.con_pac_var, "")
        self.con_cb.pack(fill="x", pady=5)
        self._update_cbs()
        
        self.con_f = self._input(f, "Fecha Manual (YYYY-MM-DD):")
        self.con_f.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.con_s = self._input(f, "Síntomas Reportados:")
        self.con_s.bind("<KeyRelease>", lambda e: self._h_live_triage()) # Innovación: Triage en vivo
        
        # Panel de Triage IA (Innovación)
        self.triage_frame = tk.Frame(f, bg="#ecf0f1", pady=10, padx=10, relief="flat")
        self.triage_frame.pack(fill="x", pady=10)
        self.triage_lbl = tk.Label(self.triage_frame, text="IA: Esperando síntomas...", 
                                   bg="#ecf0f1", font=("Segoe UI", 9, "italic"))
        self.triage_lbl.pack()

        self.con_d = self._input(f, "Diagnóstico Médico:")
        self.con_t = self._input(f, "Tratamiento / Receta:")
        
        tk.Button(f, text="FINALIZAR Y GUARDAR", bg="#3498db", fg="white", 
                  command=self._h_con).pack(fill="x", pady=(10, 5))
        
        tk.Button(f, text="BORRAR DATOS", bg="#95a5a6", fg="white", 
                  command=self._limpiar_con).pack(fill="x", pady=5)

    def _ui_busqueda(self, m):
        """Crea la tabla interactiva para búsqueda avanzada de pacientes."""
        b = tk.Frame(m, bg="#f0f2f5", pady=20, padx=20)
        b.pack(fill="x")
        self.src_e = tk.Entry(b, width=40)
        self.src_e.pack(side="left", padx=10)
        self.src_e.bind("<KeyRelease>", lambda e: self._h_search())
        
        self.src_m = tk.StringVar(value="Nombre")
        ttk.OptionMenu(b, self.src_m, "Nombre", "Nombre", "Edad", "Diagnóstico").pack(side="left")
        
        # Uso de Treeview para visualización tabular de datos
        self.tree = ttk.Treeview(m, columns=("N","E","G","C"), show="headings")
        for c, t in zip(("N","E","G","C"), ("Nombre","Edad","Género","Visitas")):
            self.tree.heading(c, text=t.upper())
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree.bind("<Double-1>", self._h_hist) # Ver historial completo al hacer doble clic

    def _ui_analisis(self, m):
        """Layout del módulo de Inteligencia de Datos (Hub de Analytics)."""
        p = tk.Frame(m, bg="#f0f2f5", padx=20, pady=20)
        p.pack(fill="both", expand=True)
        
        btns = tk.Frame(p, bg="#f0f2f5")
        btns.pack(side="left", fill="y", padx=(0,20))
        
        # Botones de reporte
        ops = [("🩺 Patologías", self._h_an1), ("👥 Prom. Edad", self._h_an2), 
               ("📈 Evolución", self._h_an3), ("🔝 Más Frecuentes", self._h_an4), ("✨ Predicción IA", self._h_an5)]
        for t, c in ops:
            tk.Button(btns, text=t, command=c, width=15, relief="groove").pack(pady=5)
            
        self.viz = tk.Frame(p, bg="white") # Panel donde se renderizan los gráficos de Matplotlib
        self.viz.pack(side="right", fill="both", expand=True)

    # --- MANEJADORES DE EVENTOS (HANDLERS) ---
    
    def _actualizar_dashboard(self):
        """Refresca todos los indicadores y gráficos de la pantalla de inicio."""
        pacs = self.gestor.obtener_todos_los_pacientes()
        self.lbl_p.config(text=str(len(pacs)))
        self.lbl_c.config(text=str(sum(len(p.consultas) for p in pacs)))
        
        self._clear_viz_container(self.plot_dash)
        res = self.analisis.obtener_enfermedades_comunes()
        
        # Validación para evitar errores de renderizado en Matplotlib con pocos datos
        if not isinstance(res, str) and not res.empty:
            fig, ax = plt.subplots(figsize=(5,3))
            # Innovación visual: Colores coordinados
            res.head(5).plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['#3498db', '#2ecc71', '#f1c40f', '#e74c3c'])
            ax.set_ylabel('')
            FigureCanvasTkAgg(fig, master=self.plot_dash).draw()
            FigureCanvasTkAgg(fig, master=self.plot_dash).get_tk_widget().pack(fill="both", expand=True)

    def _h_live_triage(self):
        """Handler innovador: Realiza análisis de riesgo en tiempo real mientras el usuario escribe."""
        texto = self.con_s.get()
        res = self.analisis._ia.realizar_triage(texto)
        
        # Actualización dinámica de la interfaz
        self.triage_lbl.config(text=res["mensaje"], fg=res["color"])
        self.triage_frame.config(highlightbackground=res["color"], highlightthickness=2)

    def _h_reg(self):
        """Valida y procesa el registro de un nuevo paciente."""
        try:
            n, e, g, h = self.reg_n.get(), int(self.reg_e.get()), self.reg_g.get(), self.reg_h.get("1.0","end-1c")
            if not n: raise ValueError("Nombre vacío")
            self.gestor.registrar_paciente(Paciente(n, e, g, h))
            self.gestor.guardar_datos()
            messagebox.showinfo("Confirmación", "Paciente dado de alta correctamente")
            self._limpiar_reg() # Interactividad: Limpiar tras éxito
            self._update_cbs()
        except: messagebox.showerror("Error", "Datos del paciente incompletos o inválidos")

    def _limpiar_reg(self):
        """Limpia los campos del formulario de registro."""
        self.reg_n.delete(0, "end")
        self.reg_e.delete(0, "end")
        self.reg_h.delete("1.0", "end")

    def _update_cbs(self):
        """Actualiza la lista desplegable de pacientes disponibles para consulta."""
        names = [p.nombre for p in self.gestor.obtener_todos_los_pacientes()]
        menu = self.con_cb["menu"]; menu.delete(0, "end")
        for n in names: menu.add_command(label=n, command=lambda v=n: self.con_pac_var.set(v))
        if names: self.con_pac_var.set(names[-1])

    def _h_con(self):
        """Procesa y vincula una consulta médica al paciente seleccionado."""
        p = self.gestor.buscar_paciente_por_nombre(self.con_pac_var.get())
        if p:
            c = Consulta(self.con_f.get(), self.con_s.get(), self.con_d.get(), self.con_t.get())
            p.agregar_consulta(c)
            self.gestor.guardar_datos()
            messagebox.showinfo("Éxito", f"Consulta guardada para {p.nombre}")
            self._limpiar_con() # Interactividad: Limpiar tras éxito
        else: messagebox.showwarning("Atención", "Debe seleccionar un paciente primero")

    def _limpiar_con(self):
        """Limpia los campos del formulario de consulta."""
        self.con_s.delete(0, "end")
        self.con_d.delete(0, "end")
        self.con_t.delete(0, "end")
        self.con_f.delete(0, "end")
        self.con_f.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def _h_search(self):
        """Ejecuta la búsqueda en tiempo real mientras el usuario escribe."""
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in self.gestor.buscar_avanzado(self.src_e.get(), self.src_m.get()):
            self.tree.insert("", "end", values=(p.nombre, p.edad, p.genero, len(p.consultas)))

    def _h_hist(self, e):
        """Abre una ventana secundaria con el historial completo del paciente seleccionado."""
        sel = self.tree.selection()
        if not sel: return
        p = self.gestor.buscar_paciente_por_nombre(self.tree.item(sel[0], "values")[0])
        top = tk.Toplevel(self); top.title(f"Historial - {p.nombre}")
        t = tk.Text(top, padx=10, pady=10); t.pack(fill="both", expand=True)
        t.insert("1.0", p.mostrar_historial_completo())
        t.config(state="disabled")

    def _clear_viz_container(self, container):
        """Limpia un contenedor de sus widgets internos (útil para refrescar gráficos)."""
        for w in container.winfo_children(): w.destroy()

    def _clear_viz(self): self._clear_viz_container(self.viz)

    # --- HANDLERS DE ANÁLISIS ---
    
    def _h_an1(self):
        """Reporte de enfermedades (Texto Pandas)."""
        self._clear_viz(); t = tk.Text(self.viz, font=("Consolas", 10), padx=20, pady=20); t.pack(fill="both")
        t.insert("1.0", "--- FRECUENCIA DE DIAGNÓSTICOS ---\n\n")
        t.insert("end", str(self.analisis.obtener_enfermedades_comunes()))

    def _h_an2(self):
        """Gráfico de Edad Promedio (Matplotlib)."""
        self._clear_viz(); res = self.analisis.obtener_edad_promedio_diagnostico()
        if res is not None:
            fig, ax = plt.subplots(figsize=(6,4)); res.plot(kind='bar', ax=ax, color='#3498db')
            ax.set_title("Edad Promedio según Patología")
            plt.xticks(rotation=45)
            FigureCanvasTkAgg(fig, master=self.viz).get_tk_widget().pack(fill="both", expand=True)

    def _h_an3(self):
        """Gráfico de Tendencia Temporal (Matplotlib)."""
        self._clear_viz(); df = self.analisis._preparar_dataset()
        if df is not None:
            fig, ax = plt.subplots(); df.sort_values('Fecha').set_index('Fecha').resample('ME').size().plot(ax=ax, marker='o')
            ax.set_title("Evolución de Visitas Mensuales")
            FigureCanvasTkAgg(fig, master=self.viz).get_tk_widget().pack(fill="both", expand=True)

    def _h_an4(self):
        """Reporte de Pacientes Frecuentes (Texto Pandas)."""
        self._clear_viz(); t = tk.Text(self.viz, font=("Consolas", 10), padx=20, pady=20); t.pack()
        t.insert("1.0", str(self.analisis.obtener_pacientes_frecuentes()))

    def _h_an5(self):
        """Reporte Inteligente de IA Predictiva."""
        self._clear_viz(); t = tk.Text(self.viz, font=("Segoe UI", 11), padx=20, pady=20); t.pack(fill="both")
        t.insert("1.0", self.analisis.obtener_sugerencias_ia())

if __name__ == "__main__":
    app = BUAPMedicineApp()
    app.mainloop()
