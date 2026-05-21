import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime

# Matplotlib para integración en GUI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.dates as mdates
import textwrap

# Ajustar path para importar módulos locales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.paciente import Paciente
from clases.consulta import Consulta
from logica.gestor_consultorio import GestorConsultorio
from logica.analizador_salud import AnalizadorSalud
from ml.ia_preventiva import ModeloPreventivo

class BUAPMedicineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("BUAP Medicine - Premium Edition")
        self.geometry("1100x800")
        self.configure(bg="#f0f2f5")
        
        # Persistencia y Lógica
        self.gestor = GestorConsultorio()
        self.analizador = AnalizadorSalud(self.gestor)
        self.modelo_ia = ModeloPreventivo()  # Motor de IA Preventiva
        
        self.nav_buttons = {}  # Seguimiento de botones para estado activo
        self.current_view = None
        
        self._setup_styles()
        self._setup_layout()
        self._setup_navigation_buttons()
        self._setup_frames()
        self._setup_statusbar()
        
        # Mostrar dashboard por defecto
        self.show_frame("dashboard")

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Paleta de Colores Moderna (Slate & Indigo)
        self.primary_color = "#4f46e5"    # Indigo 600
        self.sidebar_color = "#1e293b"   # Slate 800
        self.secondary_color = "#6366f1"  # Indigo 500
        self.accent_color = "#10b981"     # Emerald 500
        self.bg_color = "#f8fafc"         # Slate 50
        self.text_main = "#1e293b"        # Slate 800
        self.text_dim = "#64748b"         # Slate 500
        self.border_color = "#e2e8f0"     # Slate 200

        # Estilo de Frames
        self.style.configure("Main.TFrame", background=self.bg_color)
        self.style.configure("Sidebar.TFrame", background=self.sidebar_color)
        
        # Configuración Global de Fuentes
        self.font_h1 = ("Segoe UI", 24, "bold")
        self.font_h2 = ("Segoe UI", 18, "bold")
        self.font_h3 = ("Segoe UI", 12, "bold")
        self.font_body = ("Segoe UI", 10)
        self.font_ui = ("Segoe UI", 11)

        # Estilo de Treeview (Tablas)
        self.style.configure("Treeview", 
                           font=self.font_body, 
                           rowheight=35,
                           background="white",
                           fieldbackground="white",
                           borderwidth=0)
        self.style.configure("Treeview.Heading", 
                           font=self.font_h3, 
                           background="#f1f5f9", 
                           foreground=self.text_main,
                           relief="flat")
        self.style.map("Treeview", background=[('selected', self.primary_color)])

        # Estilo de Scrollbar Moderno (Fino y Minimalista)
        self.style.layout("Modern.Vertical.TScrollbar",
                          [('Vertical.Scrollbar.trough',
                            {'children': [('Vertical.Scrollbar.thumb',
                                           {'expand': '1', 'sticky': 'nswe'})],
                             'sticky': 'ns'})])
        self.style.configure("Modern.Vertical.TScrollbar", 
                             background="#cbd5e1", 
                             troughcolor=self.bg_color,
                             borderwidth=0,
                             relief="flat",
                             width=6)
        self.style.map("Modern.Vertical.TScrollbar",
                       background=[('active', self.primary_color)])

    def _setup_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = tk.Frame(self, bg=self.sidebar_color, width=260)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Container para TopBar + Workspace
        self.right_container = tk.Frame(self, bg=self.bg_color)
        self.right_container.grid(row=0, column=1, sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        # TOP BAR
        self.top_bar = tk.Frame(self.right_container, bg="white", height=70, 
                                highlightthickness=1, highlightbackground=self.border_color)
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)
        
        self.view_title_var = tk.StringVar(value="Dashboard")
        tk.Label(self.top_bar, textvariable=self.view_title_var, font=self.font_h2,
                 bg="white", fg=self.text_main, padx=30).pack(side="left")
        
        # Main Workspace
        self.main_area = tk.Frame(self.right_container, bg=self.bg_color)
        self.main_area.grid(row=1, column=0, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

    def _setup_statusbar(self):
        self.status_var = tk.StringVar(value="Sincronizado | Conexión Local Estable")
        self.status_bar = tk.Label(self, textvariable=self.status_var, bd=0, 
                                   anchor="e", bg="white", fg=self.text_dim, 
                                   font=("Segoe UI", 8), padx=20, pady=5)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def _setup_navigation_buttons(self):
        # Logo Section
        logo_frame = tk.Frame(self.sidebar, bg=self.sidebar_color, pady=40)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="🩺", font=("Segoe UI", 32), bg=self.sidebar_color).pack()
        tk.Label(logo_frame, text="CLINICA", font=("Segoe UI", 14, "bold"),
                 bg=self.sidebar_color, fg="white").pack()
        tk.Label(logo_frame, text="Intelligent Management", font=("Segoe UI", 8),
                 bg=self.sidebar_color, fg=self.secondary_color).pack()
        
        tk.Frame(self.sidebar, bg=self.secondary_color, height=1).pack(fill="x", padx=20, pady=10)

        nav_items = [
            ("🏠  Dashboard", "dashboard"),
            ("👤  Registro Paciente", "registro"),
            ("📝  Nueva Consulta", "consulta"),
            ("🔍  Búsqueda", "busqueda"),
            ("📊  Analisis", "analisis")
        ]
        
        for text, key in nav_items:
            btn = tk.Button(self.sidebar, text=text, font=self.font_ui,
                           bg=self.sidebar_color, fg="#94a3b8", relief="flat",
                           activebackground=self.primary_color, activeforeground="white",
                           padx=30, pady=15, anchor="w", cursor="hand2",
                           command=lambda k=key: self.show_frame(k))
            btn.pack(fill="x")
            self.nav_buttons[key] = btn
            
            btn.bind("<Enter>", lambda e, k=key: self._on_nav_enter(k))
            btn.bind("<Leave>", lambda e, k=key: self._on_nav_leave(k))

    def _on_nav_enter(self, key):
        if self.current_view != key:
            self.nav_buttons[key].config(bg="#334155", fg="white")

    def _on_nav_leave(self, key):
        if self.current_view != key:
            self.nav_buttons[key].config(bg=self.sidebar_color, fg="#94a3b8")
        else:
            self.nav_buttons[key].config(bg=self.primary_color, fg="white")

    def _setup_frames(self):
        self.frames = {}
        
        for F in ("dashboard", "registro", "consulta", "busqueda", "analisis"):
            frame = tk.Frame(self.main_area, bg=self.bg_color)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
            # Inicializar cada vista
            if F == "dashboard": self._init_dashboard(frame)
            elif F == "registro": self._init_registro(frame)
            elif F == "consulta": self._init_consulta(frame)
            elif F == "busqueda": self._init_busqueda(frame)
            elif F == "analisis": self._init_analisis(frame)

    def show_frame(self, name):
        if self.current_view:
            self.nav_buttons[self.current_view].config(bg=self.sidebar_color, fg="#94a3b8")
        
        self.current_view = name
        self.nav_buttons[name].config(bg=self.primary_color, fg="white")
        self.view_title_var.set(name.replace("_", " ").title())
        
        frame = self.frames[name]
        frame.tkraise()
        if name == "dashboard": self._refresh_dashboard()

    # --- VISTAS ---

    def _init_dashboard(self, master):
        container = tk.Frame(master, bg=self.bg_color, padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        # Grid de Cards
        cards_frame = tk.Frame(container, bg=self.bg_color)
        cards_frame.pack(fill="x", pady=(0, 30))
        
        self.card_pacientes = self._create_card(cards_frame, "PACIENTES", "👤", 0)
        self.card_consultas = self._create_card(cards_frame, "CONSULTAS TOTALES", "📅", 1)
        self.card_hoy = self._create_card(cards_frame, "ATENCIONES HOY", "⚡", 2)
        
        # Bottom Section
        bottom_area = tk.Frame(container, bg=self.bg_color)
        bottom_area.pack(fill="both", expand=True)
        
        # Panel Izquierdo: Gráfico
        chart_panel = tk.Frame(bottom_area, bg="white", padx=20, pady=20, 
                              highlightthickness=1, highlightbackground=self.border_color)
        chart_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        tk.Label(chart_panel, text="Actividad Reciente", font=self.font_h3, 
                 bg="white", fg=self.text_main).pack(anchor="w")
        
        self.dash_plot_frame = tk.Frame(chart_panel, bg="white")
        self.dash_plot_frame.pack(fill="both", expand=True, pady=10)
        
        # Panel Derecho: Acciones rápidas
        actions_panel = tk.Frame(bottom_area, bg="white", width=300, padx=20, pady=20,
                                 highlightthickness=1, highlightbackground=self.border_color)
        actions_panel.pack(side="right", fill="y")
        actions_panel.pack_propagate(False)
        
        tk.Label(actions_panel, text="Acciones Rápidas", font=self.font_h3, 
                 bg="white", fg=self.text_main).pack(anchor="w", pady=(0, 20))
        
        quick_btns = [
            ("➕ Nuevo Paciente", "registro"),
            ("🩺 Iniciar Consulta", "consulta"),
            ("🔍 Buscar Registro", "busqueda")
        ]
        for t, k in quick_btns:
            tk.Button(actions_panel, text=t, font=self.font_ui, bg=self.primary_color, fg="white",
                      relief="flat", pady=10, cursor="hand2",
                      command=lambda k=k: self.show_frame(k)).pack(fill="x", pady=5)
            
        tk.Button(actions_panel, text="🔄 Actualizar Todo", command=self._refresh_dashboard,
                  bg="white", fg=self.text_dim, font=self.font_body, relief="flat").pack(side="bottom", fill="x")

    def _create_card(self, parent, title, icon, col):
        card = tk.Frame(parent, bg="white", padx=25, pady=25, 
                        highlightthickness=1, highlightbackground=self.border_color)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        header = tk.Frame(card, bg="white")
        header.pack(fill="x")
        
        tk.Label(header, text=icon, font=("Segoe UI", 16), bg="white").pack(side="left")
        tk.Label(header, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg=self.text_dim, padx=10).pack(side="left")
        
        lbl_val = tk.Label(card, text="0", font=("Segoe UI", 28, "bold"), bg="white", fg=self.text_main)
        lbl_val.pack(anchor="w", pady=(15, 0))
        
        return lbl_val

    def _init_registro(self, master):
        container = tk.Frame(master, bg=self.bg_color, padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        form_card = tk.Frame(container, bg="white", padx=50, pady=50, 
                             highlightthickness=1, highlightbackground=self.border_color)
        form_card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(form_card, text="Crear Expediente de Paciente", font=self.font_h2, 
                 bg="white", fg=self.text_main).pack(pady=(0, 10))
        tk.Label(form_card, text="Complete la información básica para el historial clínico", 
                 font=self.font_body, bg="white", fg=self.text_dim).pack(pady=(0, 30))
        
        # Grid para el formulario
        grid_f = tk.Frame(form_card, bg="white")
        grid_f.pack(fill="x")
        
        fields = [
            ("👤 Nombre Completo", "Nombre Completo:", "entry"),
            ("📅 Edad", "Edad:", "entry"),
            ("⚧ Género", "Género:", "option"),
            ("📜 Antecedentes Médicos", "Historial Médico:", "text")
        ]
        self.reg_inputs = {}
        
        for i, (icon_text, label, type) in enumerate(fields):
            row_f = tk.Frame(grid_f, bg="white")
            row_f.pack(fill="x", pady=8)
            
            tk.Label(row_f, text=icon_text, font=("Segoe UI", 9, "bold"), 
                     bg="white", fg=self.text_main).pack(anchor="w")
            
            if type == "entry":
                ent = tk.Entry(row_f, font=self.font_ui, bg="#f8fafc", relief="flat", 
                               highlightthickness=1, highlightbackground=self.border_color)
                ent.pack(fill="x", ipady=8, pady=(5, 0))
                self.reg_inputs[label] = ent
            elif type == "option":
                var = tk.StringVar(value="Masculino")
                opt = ttk.OptionMenu(row_f, var, "Masculino", "Masculino", "Femenino", "Otro")
                opt.pack(fill="x", pady=(5, 0))
                self.reg_inputs[label] = var
            elif type == "text":
                txt = tk.Text(row_f, height=4, font=self.font_body, bg="#f8fafc", relief="flat", 
                              highlightthickness=1, highlightbackground=self.border_color)
                txt.pack(fill="x", pady=(5, 0))
                self.reg_inputs[label] = txt
                
        tk.Button(form_card, text="💾 GUARDAR EXPEDIENTE", command=self._h_registrar_paciente,
                  bg=self.accent_color, fg="white", font=("Segoe UI", 11, "bold"), 
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=(30, 10))
        
        tk.Button(form_card, text="Limpiar Formulario", command=self._clear_registration,
                  bg="white", fg=self.text_dim, font=self.font_body, relief="flat").pack()

    def _init_consulta(self, master):
        main_container = tk.Frame(master, bg=self.bg_color, padx=40, pady=20)
        main_container.pack(fill="both", expand=True)
        
        # Dos columnas: Formulario e IA Live
        content = tk.Frame(main_container, bg=self.bg_color)
        content.pack(fill="both", expand=True)
        
        # Columna 1: Formulario
        form_frame = tk.Frame(content, bg="white", padx=40, pady=40, 
                              highlightthickness=1, highlightbackground=self.border_color)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        tk.Label(form_frame, text="Información de la Consulta", font=self.font_h3, 
                 bg="white", fg=self.text_main).pack(anchor="w", pady=(0, 20))
        
        tk.Label(form_frame, text="Paciente", font=("Segoe UI", 9, "bold"), bg="white", fg=self.text_dim).pack(anchor="w")
        self.pac_var = tk.StringVar()
        self.cb_paciente = ttk.OptionMenu(form_frame, self.pac_var, "")
        self.cb_paciente.pack(pady=(0, 20), fill="x")
        self._update_pac_cb()
        
        labels = [("📅 Fecha de Atención", "Fecha (YYYY-MM-DD):"), 
                  ("🤒 Síntomas Reportados", "Síntomas:"), 
                  ("🔍 Diagnóstico Médico", "Diagnóstico:"), 
                  ("💊 Plan de Tratamiento", "Tratamiento:")]
        self.con_inputs = {}
        
        for icon_lbl, field_key in labels:
            tk.Label(form_frame, text=icon_lbl, font=("Segoe UI", 9, "bold"), bg="white", fg=self.text_dim).pack(anchor="w")
            ent = tk.Entry(form_frame, font=self.font_ui, bg="#f8fafc", relief="flat", highlightthickness=1, highlightbackground=self.border_color)
            ent.pack(pady=(0, 15), fill="x", ipady=8)
            if "Fecha" in field_key: ent.insert(0, datetime.now().strftime("%Y-%m-%d"))
            if "Síntomas" in field_key: ent.bind("<KeyRelease>", self._h_live_ia_triage)
            self.con_inputs[field_key] = ent
            
        tk.Button(form_frame, text="CONFIRMAR Y GUARDAR REGISTRO", command=self._h_registrar_consulta,
                  bg=self.primary_color, fg="white", font=("Segoe UI", 11, "bold"), 
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=10)

        # Columna 2: Panel IA Live (Visualmente mejorado como un Scanner)
        self.ia_live_frame = tk.Frame(content, bg=self.sidebar_color, padx=30, pady=30, width=380)
        self.ia_live_frame.pack(side="right", fill="both")
        self.ia_live_frame.pack_propagate(False)
        
        tk.Label(self.ia_live_frame, text="SCANNER IA PREVENTIVA", font=("Segoe UI", 10, "bold"), 
                 bg=self.sidebar_color, fg=self.accent_color).pack(pady=(0, 20))
        
        # Un separador visual tipo terminal
        tk.Frame(self.ia_live_frame, bg="#334155", height=1).pack(fill="x", pady=10)

        self.ia_status_lbl = tk.Label(self.ia_live_frame, text="ESPERANDO ENTRADA DE SÍNTOMAS...", 
                                     font=("Consolas", 10), bg=self.sidebar_color, fg="#94a3b8", 
                                     wraplength=300, justify="left")
        self.ia_status_lbl.pack(pady=30, fill="x")
        
        self.ia_indicator = tk.Frame(self.ia_live_frame, height=4, bg="#334155")
        self.ia_indicator.pack(fill="x", side="bottom")

    def _h_live_ia_triage(self, event):
        """Handler para el análisis en tiempo real con feedback visual agresivo."""
        texto = self.con_inputs["Síntomas:"].get()
        if not texto.strip():
            self.ia_status_lbl.config(text="ESPERANDO ENTRADA DE SÍNTOMAS...", fg="#94a3b8")
            self.ia_indicator.config(bg="#334155")
            return
            
        resultado = self.modelo_ia.realizar_triage(texto)
        self.ia_status_lbl.config(text=f"> ANÁLISIS EN CURSO...\n\nRESULTADO: {resultado['nivel'].upper()}\n\nDETALLE:\n{resultado['mensaje'].upper()}", 
                                     fg=resultado["color"])
        self.ia_indicator.config(bg=resultado["color"])

    def _custom_alert(self, title, message, alert_type="success"):
        """Crea una alerta moderna y personalizada que coincide con la estética de la app."""
        top = tk.Toplevel(self)
        top.title(title)
        top.geometry("400x280") # Aumentado para que el botón se vea bien
        top.resizable(False, False)
        top.configure(bg="white")
        top.transient(self)
        top.grab_set()
        
        # Centrar respecto a la ventana principal
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 140
        top.geometry(f"+{x}+{y}")

        color = self.primary_color if alert_type == "success" else "#ef4444"
        icon = "✅" if alert_type == "success" else "⚠️"

        main_f = tk.Frame(top, bg="white", padx=30, pady=25)
        main_f.pack(fill="both", expand=True)

        icon_lbl = tk.Label(main_f, text=icon, font=("Segoe UI", 40), bg="white", fg=color)
        icon_lbl.pack(pady=(0, 10))

        tk.Label(main_f, text=title.upper(), font=("Segoe UI", 11, "bold"), bg="white", fg=color).pack()
        tk.Label(main_f, text=message, font=("Segoe UI", 10), bg="white", fg=self.text_main, wraplength=340, justify="center").pack(pady=15)

        btn_f = tk.Frame(main_f, bg="white")
        btn_f.pack(side="bottom", pady=(5, 0))

        btn = tk.Button(btn_f, text="ENTENDIDO", font=("Segoe UI", 9, "bold"), 
                        bg=color, fg="white", relief="flat", padx=30, pady=10, 
                        width=15, cursor="hand2", command=top.destroy)
        btn.pack()

    def _init_busqueda(self, master):
        container = tk.Frame(master, bg=self.bg_color, padx=40, pady=20)
        container.pack(fill="both", expand=True)
        
        # Barra de Búsqueda Moderna
        search_card = tk.Frame(container, bg="white", padx=20, pady=20,
                               highlightthickness=1, highlightbackground=self.border_color)
        search_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(search_card, text="🔍", font=("Segoe UI", 14), bg="white").pack(side="left", padx=(0, 10))
        
        self.ent_search = tk.Entry(search_card, font=self.font_ui, bg="#f1f5f9", relief="flat", width=40)
        self.ent_search.pack(side="left", padx=10, ipady=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self._h_buscar())
        
        tk.Label(search_card, text="Filtrar por:", font=self.font_body, bg="white", fg=self.text_dim).pack(side="left", padx=(20, 10))
        
        self.search_mode = tk.StringVar(value="Nombre")
        search_opt = ttk.OptionMenu(search_card, self.search_mode, "Nombre", "Nombre", "Edad", "Diagnóstico")
        search_opt.pack(side="left")
        
        tk.Button(search_card, text="Limpiar", command=lambda: self._h_buscar(True),
                  bg="white", fg=self.text_dim, relief="flat", font=self.font_body).pack(side="right")
        
        # Tabla de Resultados
        table_card = tk.Frame(container, bg="white", highlightthickness=1, highlightbackground=self.border_color)
        table_card.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(table_card, columns=("N", "E", "G", "C"), show="headings")
        self.tree.heading("N", text="Paciente")
        self.tree.heading("E", text="Edad")
        self.tree.heading("G", text="Género")
        self.tree.heading("C", text="N° Consultas")
        
        # Ajustar columnas
        self.tree.column("N", width=300)
        self.tree.column("E", width=100, anchor="center")
        self.tree.column("G", width=150, anchor="center")
        self.tree.column("C", width=150, anchor="center")
        
        self.tree.tag_configure('oddrow', background='#f8fafc')
        self.tree.tag_configure('evenrow', background='white')
        
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)
        self.tree.bind("<Double-1>", self._h_ver_historial)

    def _init_analisis(self, master):
        container = tk.Frame(master, bg=self.bg_color, padx=40, pady=20)
        container.pack(fill="both", expand=True)
        
        # Layout dividido
        side_panel = tk.Frame(container, bg="white", width=250, padx=15, pady=25,
                              highlightthickness=1, highlightbackground=self.border_color)
        side_panel.pack(side="left", fill="y", padx=(0, 20))
        side_panel.pack_propagate(False)
        
        tk.Label(side_panel, text="Módulos Clínicos", font=self.font_h3, 
                 bg="white", fg=self.text_main).pack(anchor="w", padx=10, pady=(0, 25))
        
        self.analysis_btns = {}
        self.current_analysis_btn = None
        
        sections = [
            ("📊 VISUALIZACIONES", [
                ("Edad / Patología", self._h_plot_dist, "dist"),
                ("Línea de Tiempo", self._h_plot_tend, "tend")
            ]),
            ("📄 REPORTES DATA", [
                ("Enfermedades", self._h_report_pandas, "diag"),
                ("Frecuentes", self._h_report_frecuentes, "frec"),
                ("Promedios", self._h_report_edad_promedio, "prom")
            ]),
            ("✨ INTELIGENCIA IA", [
                ("Predicciones IA", self._h_ia_preventiva, "ia")
            ])
        ]
        
        for section_title, btns in sections:
            tk.Label(side_panel, text=section_title, font=("Segoe UI", 7, "bold"),
                     bg="white", fg=self.text_dim, pady=10).pack(anchor="w", padx=10)
            
            for text, cmd, key in btns:
                btn_container = tk.Frame(side_panel, bg="white")
                btn_container.pack(fill="x", pady=2)
                
                # Indicador de selección lateral
                indicator = tk.Frame(btn_container, bg="white", width=4)
                indicator.pack(side="left", fill="y")
                
                btn = tk.Button(btn_container, text=f"  {text}", command=lambda c=cmd, k=key: self._on_analysis_click(c, k),
                                font=self.font_body, bg="white", fg=self.text_main, 
                                relief="flat", anchor="w", padx=10, pady=10, cursor="hand2")
                btn.pack(side="left", fill="x", expand=True)
                
                self.analysis_btns[key] = (btn, indicator)
                
                btn.bind("<Enter>", lambda e, k=key: self._on_analysis_hover(k, True))
                btn.bind("<Leave>", lambda e, k=key: self._on_analysis_hover(k, False))
            
        self.viz_area = tk.Frame(container, bg="white", highlightthickness=1, highlightbackground=self.border_color)
        self.viz_area.pack(side="right", fill="both", expand=True)

    def _on_analysis_click(self, command, key):
        # Reset anterior
        if self.current_analysis_btn:
            b, ind = self.analysis_btns[self.current_analysis_btn]
            b.config(bg="white", fg=self.text_main, font=self.font_body)
            ind.config(bg="white")
            
        # Activar nuevo
        self.current_analysis_btn = key
        b, ind = self.analysis_btns[key]
        b.config(bg="#f1f5f9", fg=self.primary_color, font=("Segoe UI", 10, "bold"))
        ind.config(bg=self.primary_color)
        
        command()

    def _on_analysis_hover(self, key, entering):
        if self.current_analysis_btn == key: return
        
        btn, _ = self.analysis_btns[key]
        if entering:
            btn.config(bg="#f8fafc", fg=self.primary_color)
        else:
            btn.config(bg="white", fg=self.text_main)

    # --- HANDLERS ---

    def _refresh_dashboard(self):
        pacs = self.gestor.obtener_todos_los_pacientes()
        self.card_pacientes.config(text=str(len(pacs)))
        
        total_c = sum(len(p.consultas) for p in pacs)
        self.card_consultas.config(text=str(total_c))
        
        hoy = datetime.now().strftime("%Y-%m-%d")
        hoy_c = sum(1 for p in pacs for c in p.consultas if c.fecha == hoy)
        self.card_hoy.config(text=str(hoy_c))
        
        # Mini gráfico en dashboard
        for w in self.dash_plot_frame.winfo_children(): w.destroy()
        df = self.analizador._preparar_dataset()
        if df is not None:
            fig, ax = plt.subplots(figsize=(5, 3), dpi=80)
            df['Diagnostico'].value_counts().head(5).plot(kind='pie', autopct='%1.1f%%', ax=ax)
            ax.set_title("Especialidades más consultadas")
            ax.set_ylabel('')
            canvas = FigureCanvasTkAgg(fig, master=self.dash_plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

    def _h_registrar_paciente(self):
        try:
            n = self.reg_inputs["Nombre Completo:"].get()
            e = int(self.reg_inputs["Edad:"].get())
            g = self.reg_inputs["Género:"].get()
            h = self.reg_inputs["Historial Médico:"].get("1.0", "end-1c").strip()
            
            if not n: raise ValueError
            
            nuevo = Paciente(n, e, g, h)
            self.gestor.registrar_paciente(nuevo)
            self.gestor.guardar_datos()
            self._custom_alert("Éxito", f"El paciente {n} ha sido registrado correctamente en la base de datos clínica.", "success")
            self._update_pac_cb()
            self._clear_registration()
        except Exception:
            self._custom_alert("Error de Validación", "Verifique que todos los campos sean correctos y que la edad sea un número válido.", "error")

    def _clear_registration(self):
        self.reg_inputs["Nombre Completo:"].delete(0, "end")
        self.reg_inputs["Edad:"].delete(0, "end")
        self.reg_inputs["Historial Médico:"].delete("1.0", "end")

    def _update_pac_cb(self):
        names = [p.nombre for p in self.gestor.obtener_todos_los_pacientes()]
        menu = self.cb_paciente["menu"]
        menu.delete(0, "end")
        for n in names:
            menu.add_command(label=n, command=lambda v=n: self.pac_var.set(v))
        if names: self.pac_var.set(names[-1])
        else: self.pac_var.set("No hay pacientes")

    def _h_registrar_consulta(self):
        nombre = self.pac_var.get()
        paciente = self.gestor.buscar_paciente_por_nombre(nombre)
        if paciente:
            try:
                sintomas_texto = self.con_inputs["Síntomas:"].get()
                c = Consulta(
                    self.con_inputs["Fecha (YYYY-MM-DD):"].get(),
                    sintomas_texto,
                    self.con_inputs["Diagnóstico:"].get(),
                    self.con_inputs["Tratamiento:"].get()
                )
                paciente.agregar_consulta(c)
                self.gestor.guardar_datos()
                self._custom_alert("Éxito", f"Se ha registrado la consulta de {nombre} exitosamente.", "success")
                for ent in self.con_inputs.values(): 
                    if hasattr(ent, 'delete'): ent.delete(0, "end")
                self.con_inputs["Fecha (YYYY-MM-DD):"].insert(0, datetime.now().strftime("%Y-%m-%d"))
                # --- TRIAGE AUTOMÁTICO CON IA ---
                self._mostrar_triage(sintomas_texto)
            except Exception:
                self._custom_alert("Error", "No se pudo registrar la consulta. Verifique los datos ingresados.", "error")
        else:
            self._custom_alert("Atención", "Debe seleccionar un paciente antes de registrar una consulta.", "error")

    def _mostrar_triage(self, sintomas):
        """Muestra una ventana modal premium con el resultado del triage."""
        resultado = self.modelo_ia.realizar_triage(sintomas)
        if resultado["nivel"] == "N/A": return

        top = tk.Toplevel(self)
        top.title("Clinical Alert - AI Triage")
        top.geometry("450x300")
        top.configure(bg="white")
        top.grab_set()

        # Header de Alerta
        header = tk.Frame(top, bg=resultado["color"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="ANÁLISIS DE RIESGO IA", font=("Segoe UI", 10, "bold"), 
                 bg=resultado["color"], fg="white").pack(pady=(15, 0))
        tk.Label(header, text=resultado['nivel'].upper(), font=("Segoe UI", 20, "bold"), 
                 bg=resultado["color"], fg="white").pack()

        # Contenido
        body = tk.Frame(top, bg="white", padx=30, pady=30)
        body.pack(fill="both", expand=True)
        
        tk.Label(body, text=resultado["mensaje"], font=self.font_ui, 
                 bg="white", fg=self.text_main, wraplength=380).pack()
        
        tk.Button(top, text="CONFIRMAR RECEPCIÓN", command=top.destroy,
                  bg=self.sidebar_color, fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", pady=10, padx=40).pack(pady=20)

    def _h_ver_historial(self, event):
        """Muestra una ventana modal premium con el expediente completo y diseño de tarjetas."""
        item = self.tree.selection()
        if not item: return
        nombre = self.tree.item(item[0], "values")[0]
        p = self.gestor.buscar_paciente_por_nombre(nombre)
        
        if p:
            top = tk.Toplevel(self)
            top.title(f"Expediente Clínico: {p.nombre}")
            top.geometry("850x750")
            top.configure(bg=self.bg_color)
            top.grab_set()
            
            # --- HEADER PREMIUM ---
            header_outer = tk.Frame(top, bg="white", highlightthickness=1, highlightbackground=self.border_color)
            header_outer.pack(fill="x")
            
            header = tk.Frame(header_outer, bg="white", padx=40, pady=30)
            header.pack(fill="x")
            
            # Avatar circular (simulado con label)
            avatar_f = tk.Frame(header, bg=self.primary_color, width=64, height=64)
            avatar_f.pack(side="left", padx=(0, 25))
            avatar_f.pack_propagate(False)
            tk.Label(avatar_f, text=p.nombre[0].upper(), font=("Segoe UI", 24, "bold"), bg=self.primary_color, fg="white").pack(expand=True)
            
            info_f = tk.Frame(header, bg="white")
            info_f.pack(side="left", fill="both")
            
            tk.Label(info_f, text=p.nombre.upper(), font=("Segoe UI", 22, "bold"), bg="white", fg=self.text_main).pack(anchor="w")
            
            meta_f = tk.Frame(info_f, bg="white")
            meta_f.pack(anchor="w", pady=(5, 0))
            
            tk.Label(meta_f, text=f"ID: PAC-{id(p)%10000:04d}", font=("Consolas", 9), bg="#f1f5f9", fg=self.text_dim, padx=8).pack(side="left", padx=(0, 15))
            tk.Label(meta_f, text=f"🎂 {p.edad} AÑOS", font=("Segoe UI", 9, "bold"), bg="white", fg=self.text_dim).pack(side="left", padx=(0, 15))
            tk.Label(meta_f, text=f"⚧ {p.genero.upper()}", font=("Segoe UI", 9, "bold"), bg="white", fg=self.text_dim).pack(side="left")

            # --- ÁREA DE CONTENIDO SCROLLABLE ---
            content_container = tk.Frame(top, bg=self.bg_color, padx=40, pady=30)
            content_container.pack(fill="both", expand=True)
            
            canvas = tk.Canvas(content_container, bg=self.bg_color, highlightthickness=0)
            v_scroll = ttk.Scrollbar(content_container, orient="vertical", command=canvas.yview, style="Modern.Vertical.TScrollbar")
            scroll_frame = tk.Frame(canvas, bg=self.bg_color)
            
            scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=770) # Ancho aumentado ya que no hay barra
            canvas.configure(yscrollcommand=v_scroll.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            
            # La barra existe pero no se empaca (se oculta) para un look más limpio
            # El usuario puede hacer scroll con la rueda del ratón
            # v_scroll.pack(side="right", fill="y") 

            # Soporte para Scroll con Rueda del Ratón
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            # Bind local para evitar conflictos
            scroll_frame.bind_all("<MouseWheel>", _on_mousewheel)
            
            # Limpiar el bind al cerrar la ventana
            top.bind("<Destroy>", lambda e: top.unbind_all("<MouseWheel>"))

            # 1. SECCIÓN: ANTECEDENTES
            tk.Label(scroll_frame, text="INFORMACIÓN BASE", font=("Segoe UI", 8, "bold"), bg=self.bg_color, fg=self.text_dim).pack(anchor="w", pady=(0, 10))
            
            hist_card = tk.Frame(scroll_frame, bg="white", padx=25, pady=20, highlightthickness=1, highlightbackground=self.border_color)
            hist_card.pack(fill="x", pady=(0, 30))
            
            tk.Label(hist_card, text="📜 ANTECEDENTES MÉDICOS", font=("Segoe UI", 10, "bold"), bg="white", fg=self.primary_color).pack(anchor="w", pady=(0, 10))
            
            hist_text = p.historial_medico if p.historial_medico.strip() else "No se registraron antecedentes previos."
            tk.Label(hist_card, text=hist_text, font=self.font_body, bg="white", fg=self.text_main, wraplength=680, justify="left").pack(anchor="w")

            # 2. SECCIÓN: HISTORIAL DE CONSULTAS
            tk.Label(scroll_frame, text="LÍNEA DE TIEMPO CLÍNICA", font=("Segoe UI", 8, "bold"), bg=self.bg_color, fg=self.text_dim).pack(anchor="w", pady=(0, 10))
            
            if not p.consultas:
                empty_card = tk.Frame(scroll_frame, bg="white", padx=25, pady=40, highlightthickness=1, highlightbackground=self.border_color)
                empty_card.pack(fill="x")
                tk.Label(empty_card, text="No existen consultas registradas en el sistema.", font=self.font_body, bg="white", fg=self.text_dim).pack()
            else:
                # Mostrar consultas (de más reciente a más antigua)
                for i, con in enumerate(reversed(p.consultas)):
                    num_visita = len(p.consultas) - i
                    self._render_history_visit_card(scroll_frame, num_visita, con)

    def _render_history_visit_card(self, parent, index, con):
        """Renderiza una tarjeta de visita individual en el historial."""
        card_outer = tk.Frame(parent, bg=self.bg_color)
        card_outer.pack(fill="x", pady=8)
        
        # Línea de tiempo lateral (Decorativo)
        timeline_f = tk.Frame(card_outer, bg=self.bg_color, width=40)
        timeline_f.pack(side="left", fill="y")
        
        dot = tk.Frame(timeline_f, bg=self.secondary_color, width=12, height=12)
        dot.place(relx=0.5, y=25, anchor="center")
        
        line = tk.Frame(timeline_f, bg=self.border_color, width=2)
        line.pack(fill="y", padx=18)
        
        # Tarjeta Principal
        card = tk.Frame(card_outer, bg="white", padx=25, pady=20, highlightthickness=1, highlightbackground=self.border_color)
        card.pack(side="left", fill="both", expand=True)
        
        # Header de la Visita
        v_header = tk.Frame(card, bg="white")
        v_header.pack(fill="x", pady=(0, 15))
        
        tk.Label(v_header, text=f"VISITA #{index}", font=("Segoe UI", 11, "bold"), bg="white", fg=self.text_main).pack(side="left")
        tk.Label(v_header, text=con.fecha, font=("Consolas", 10, "bold"), bg="#f1f5f9", fg=self.primary_color, padx=10).pack(side="right")
        
        # Cuerpo con Grid para alineación perfecta
        grid_body = tk.Frame(card, bg="white")
        grid_body.pack(fill="x")
        
        rows = [
            ("🤒 Síntomas", con.sintomas),
            ("🔍 Diagnóstico", con.diagnostico),
            ("💊 Tratamiento", con.tratamiento)
        ]
        
        for icon, value in rows:
            r_frame = tk.Frame(grid_body, bg="white")
            r_frame.pack(fill="x", pady=4)
            
            tk.Label(r_frame, text=icon, font=("Segoe UI", 9, "bold"), bg="white", fg=self.text_dim, width=15, anchor="w").pack(side="left")
            tk.Label(r_frame, text=value, font=self.font_body, bg="white", fg=self.text_main, wraplength=500, justify="left").pack(side="left", fill="x", expand=True)

    def _h_buscar(self, clean=False):
        if clean: self.ent_search.delete(0, "end")
        query = self.ent_search.get()
        mode = self.search_mode.get()
        for i in self.tree.get_children(): self.tree.delete(i)
        resultados = self.gestor.buscar_avanzado(query, mode)
        for i, p in enumerate(resultados):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(p.nombre, p.edad, p.genero, len(p.consultas)), tags=(tag,))

    def _h_plot_dist(self):
        """Gráfica: Distribución de enfermedades por edad y género (4 paneles) con optimización de texto."""
        self._clear_viz()
        df = self.analizador._preparar_dataset()
        if df is None:
            self._mostrar_texto_simple("Sin datos suficientes para generar gráficos.")
            return

        # Calcular cantidad de diagnósticos para el escalado optimizado
        n_diag = len(df['Diagnostico'].unique())
        
        # Escalado dinámico balanceado (no exagerado para evitar espacios muertos)
        h_scaled = max(10, n_diag * 0.7) 
        
        fig, axes = plt.subplots(4, 1, figsize=(10.5, h_scaled), dpi=100)
        fig.patch.set_facecolor('white')
        
        def format_labels(ax):
            # Envolvemos para legibilidad sin exagerar
            labels = [textwrap.fill(l.get_text(), width=30) for l in ax.get_yticklabels()]
            ax.set_yticklabels(labels, fontsize=10, fontweight='500')

        # 1. Promedio Edad por Diagnóstico
        ax1 = axes[0]
        edad_diag = df.groupby('Diagnostico')['Edad'].mean().sort_values()
        edad_diag.plot(kind='barh', ax=ax1, color='#4f46e5', edgecolor='white', width=0.8)
        ax1.set_title("EDAD PROMEDIO POR PATOLOGÍA", fontsize=14, fontweight='bold', color=self.text_main, pad=20)
        format_labels(ax1)
        ax1.set_xlabel("Años de Edad", fontsize=11, fontweight='bold')
        ax1.grid(axis='x', linestyle='--', alpha=0.4)
        ax1.tick_params(axis='x', labelsize=10)
        
        # 2. Distribución por Género
        ax2 = axes[1]
        genero_diag = pd.crosstab(df['Diagnostico'], df['Genero'])
        genero_diag.plot(kind='barh', stacked=True, ax=ax2, color=['#818cf8', '#10b981'], width=0.8)
        ax2.set_title("DISTRIBUCIÓN DE CASOS POR GÉNERO", fontsize=14, fontweight='bold', color=self.text_main, pad=20)
        format_labels(ax2)
        ax2.legend(fontsize=11, loc='upper right', frameon=True, shadow=True)
        ax2.grid(axis='x', linestyle='--', alpha=0.4)
        ax2.tick_params(axis='x', labelsize=10)
        
        # 3. Dispersión de Edades (Boxplot Premium)
        ax3 = axes[2]
        df.boxplot(column='Edad', by='Diagnostico', ax=ax3, vert=False, patch_artist=True, 
                   boxprops=dict(facecolor='#e0e7ff', color='#4f46e5', linewidth=1.5),
                   medianprops=dict(color='#dc2626', linewidth=2),
                   whiskerprops=dict(color='#4f46e5', linewidth=1.5))
        ax3.set_title("DISPERSIÓN Y RANGO DE EDADES", fontsize=14, fontweight='bold', color=self.text_main, pad=20)
        format_labels(ax3)
        ax3.set_xlabel("Edad del Paciente", fontsize=11, fontweight='bold')
        ax3.tick_params(axis='x', labelsize=10)
        plt.suptitle("") 
        
        # 4. Frecuencia Total (Ranking de Casos)
        ax4 = axes[3]
        counts = df['Diagnostico'].value_counts().sort_values()
        counts.plot(kind='barh', ax=ax4, color='#64748b', width=0.8)
        ax4.set_title("RANKING DE FRECUENCIA CLÍNICA (CASOS TOTALES)", fontsize=14, fontweight='bold', color=self.text_main, pad=20)
        format_labels(ax4)
        ax4.set_xlabel("Número de Consultas Registradas", fontsize=11, fontweight='bold')
        ax4.grid(axis='x', linestyle='--', alpha=0.4)
        ax4.tick_params(axis='x', labelsize=10)
        
        # Uso de Tight Layout para auto-ajustar todo y evitar recortes
        fig.tight_layout(pad=3.0)

        # Contenedor con scroll moderno (Todo Blanco)
        canvas_container = tk.Canvas(self.viz_area, bg="white", highlightthickness=0)
        v_scroll = ttk.Scrollbar(self.viz_area, orient="vertical", command=canvas_container.yview, style="Modern.Vertical.TScrollbar")
        scroll_f = tk.Frame(canvas_container, bg="white")
        
        # Guardar el ID de la ventana para poder moverla (centrarla)
        window_id = canvas_container.create_window((0, 0), window=scroll_f, anchor="nw")
        
        def _on_canvas_configure(e):
            # Ajustar región de scroll
            canvas_container.configure(scrollregion=canvas_container.bbox("all"))
            # Lógica de Centrado Dinámico
            f_width = scroll_f.winfo_reqwidth()
            if e.width > f_width:
                offset = (e.width - f_width) / 2
                canvas_container.coords(window_id, offset, 0)
            else:
                canvas_container.coords(window_id, 0, 0)

        canvas_container.bind("<Configure>", _on_canvas_configure)
        canvas_container.configure(yscrollcommand=v_scroll.set)
        
        canvas_container.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        
        canvas = FigureCanvasTkAgg(fig, master=scroll_f)
        canvas_widget = canvas.get_tk_widget()
        # Empacar sin fill horizontal para permitir el centrado
        canvas_widget.pack()
        
        # --- MEJORA DE SCROLL: Bind del mouse wheel al widget de la gráfica ---
        def _on_mousewheel(event):
            canvas_container.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_widget.bind("<MouseWheel>", _on_mousewheel)
        
        canvas.draw()
        plt.close(fig)

    def _h_plot_tend(self):
        """Gráfica: Tendencia de consultas a lo largo del tiempo (3 paneles)."""
        self._clear_viz()
        df = self.analizador._preparar_dataset()
        if df is None:
            self._mostrar_texto_simple("Sin datos suficientes para generar gráficos.")
            return

        fig, axes = plt.subplots(3, 1, figsize=(10, 10), dpi=80)
        fig.suptitle("Tendencia de Consultas a lo Largo del Tiempo",
                     fontsize=14, fontweight='bold', color='#2c3e50')
        fig.patch.set_facecolor('#f8f9fa')

        df_sorted = df.sort_values('Fecha').copy()
        df_sorted = df_sorted.set_index('Fecha')
        tendencia_mensual = df_sorted.resample('ME').size()

        # ─ Panel 1: Línea de tendencia mensual + media móvil ─
        ax1 = axes[0]
        ax1.fill_between(tendencia_mensual.index, tendencia_mensual.values,
                         alpha=0.25, color='#2ecc71')
        ax1.plot(tendencia_mensual.index, tendencia_mensual.values,
                 marker='o', color='#27ae60', linewidth=2, markersize=6, label='Consultas/mes')
        if len(tendencia_mensual) >= 2:
            rolling = tendencia_mensual.rolling(window=2, min_periods=1).mean()
            ax1.plot(rolling.index, rolling.values, color='#e74c3c', linewidth=1.5,
                     linestyle='--', label='Media móvil (2 meses)')
        for x, y in zip(tendencia_mensual.index, tendencia_mensual.values):
            ax1.annotate(str(y), (x, y), textcoords="offset points",
                         xytext=(0, 6), ha='center', fontsize=8)
        ax1.set_title("Volumen Mensual de Consultas", fontsize=10, fontweight='bold')
        ax1.set_ylabel("Consultas")
        ax1.set_facecolor('#fdfdfd')
        ax1.legend(fontsize=8)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right', fontsize=8)

        # ─ Panel 2: Barras mensuales por género ─
        ax2 = axes[1]
        df_genero = df_sorted.copy()
        df_genero['Mes'] = df_genero.index.to_period('M').astype(str)
        pivot = df_genero.groupby(['Mes', 'Genero']).size().unstack(fill_value=0)
        pivot.plot(kind='bar', ax=ax2, color=['#3498db', '#e91e8c', '#95a5a6'][:len(pivot.columns)],
                   edgecolor='white', linewidth=0.5)
        ax2.set_title("Consultas por Mes y Género", fontsize=10, fontweight='bold')
        ax2.set_ylabel("Consultas")
        ax2.set_xlabel("")
        ax2.set_facecolor('#fdfdfd')
        ax2.legend(fontsize=8)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right', fontsize=8)

        # ─ Panel 3: Consultas acumuladas en el tiempo ─
        ax3 = axes[2]
        acumulado = tendencia_mensual.cumsum()
        ax3.fill_between(acumulado.index, acumulado.values, alpha=0.3, color='#3498db')
        ax3.plot(acumulado.index, acumulado.values, marker='s', color='#2980b9',
                 linewidth=2, markersize=5, label='Total acumulado')
        ax3.set_title("Consultas Acumuladas (Total Histórico)", fontsize=10, fontweight='bold')
        ax3.set_ylabel("Total acumulado")
        ax3.set_facecolor('#fdfdfd')
        ax3.legend(fontsize=8)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=30, ha='right', fontsize=8)

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        # Frame con scroll para la gráfica alta
        frame_scroll = tk.Frame(self.viz_area)
        frame_scroll.pack(fill="both", expand=True)
        canvas = FigureCanvasTkAgg(fig, master=frame_scroll)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def _h_report_pandas(self):
        """Reporte 1: Enfermedades más comunes (Modernizado)."""
        self._clear_viz()
        serie = self.analizador.generar_reporte_enfermedades()
        if isinstance(serie, str):
            self._mostrar_texto_simple(serie)
            return

        # Encabezado Premium
        header_f = tk.Frame(self.viz_area, bg="white", pady=20)
        header_f.pack(fill="x")
        tk.Label(header_f, text="📋 RANKING DE ENFERMEDADES", font=("Segoe UI", 16, "bold"), bg="white", fg=self.text_main).pack()
        tk.Label(header_f, text=f"Se detectaron {len(serie)} diagnósticos distintos en el historial médico.", 
                 font=("Segoe UI", 10), bg="white", fg=self.text_dim).pack()

        # Contenedor Scrollable
        canvas_f = tk.Canvas(self.viz_area, bg="#f8fafc", highlightthickness=0)
        v_scroll = ttk.Scrollbar(self.viz_area, orient="vertical", command=canvas_f.yview, style="Modern.Vertical.TScrollbar")
        scroll_f = tk.Frame(canvas_f, bg="#f8fafc")
        
        scroll_f.bind("<Configure>", lambda e: canvas_f.configure(scrollregion=canvas_f.bbox("all")))
        window_id = canvas_f.create_window((0,0), window=scroll_f, anchor="nw")
        canvas_f.configure(yscrollcommand=v_scroll.set)
        
        canvas_f.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        
        # Vincular scroll de mouse
        canvas_f.bind_all("<MouseWheel>", lambda e: canvas_f.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Asegurar que el frame interior llene el ancho del canvas
        canvas_f.bind("<Configure>", lambda e: canvas_f.itemconfig(window_id, width=e.width), add="+")

        for i, (enfermedad, count) in enumerate(serie.items(), 1):
            card = tk.Frame(scroll_f, bg="white", padx=20, pady=12, highlightthickness=1, highlightbackground=self.border_color)
            card.pack(fill="x", padx=20, pady=6) # Relleno horizontal completo
            
            # Icono Técnico (Serio)
            icon_f = tk.Frame(card, bg="#f8fafc", width=40, height=40)
            icon_f.pack(side="left", padx=(0, 15))
            icon_f.pack_propagate(False)
            
            tk.Label(icon_f, text="📋", font=("Segoe UI", 12), bg="#f8fafc").pack(expand=True)
            
            # Info
            tk.Label(card, text=enfermedad.upper(), font=("Segoe UI", 10, "bold"), bg="white", fg=self.text_main).pack(side="left")
            
            # Badge de casos
            badge_f = tk.Frame(card, bg="#f1f5f9", padx=12, pady=6)
            badge_f.pack(side="right")
            tk.Label(badge_f, text=f"{count} REGISTROS", font=("Consolas", 9, "bold"), bg="#f1f5f9", fg=self.primary_color).pack()

    def _h_report_frecuentes(self):
        """Reporte 2: Pacientes frecuentes (Modernizado)."""
        self._clear_viz()
        serie = self.analizador.pacientes_frecuentes()
        if isinstance(serie, str):
            self._mostrar_texto_simple(serie)
            return

        header_f = tk.Frame(self.viz_area, bg="white", pady=20)
        header_f.pack(fill="x")
        tk.Label(header_f, text="👤 PACIENTES CON MÁS CONSULTAS", font=("Segoe UI", 16, "bold"), bg="white", fg=self.text_main).pack()
        tk.Label(header_f, text=f"Total de {len(serie)} pacientes registrados en el sistema.", 
                 font=("Segoe UI", 10), bg="white", fg=self.text_dim).pack()

        canvas_f = tk.Canvas(self.viz_area, bg="#f8fafc", highlightthickness=0)
        v_scroll = ttk.Scrollbar(self.viz_area, orient="vertical", command=canvas_f.yview, style="Modern.Vertical.TScrollbar")
        scroll_f = tk.Frame(canvas_f, bg="#f8fafc")
        
        scroll_f.bind("<Configure>", lambda e: canvas_f.configure(scrollregion=canvas_f.bbox("all")))
        window_id = canvas_f.create_window((0,0), window=scroll_f, anchor="nw")
        canvas_f.configure(yscrollcommand=v_scroll.set)
        
        canvas_f.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        
        canvas_f.bind_all("<MouseWheel>", lambda e: canvas_f.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Asegurar que el frame interior llene el ancho del canvas
        canvas_f.bind("<Configure>", lambda e: canvas_f.itemconfig(window_id, width=e.width), add="+")

        for i, (paciente, count) in enumerate(serie.items(), 1):
            card = tk.Frame(scroll_f, bg="white", padx=20, pady=12, highlightthickness=1, highlightbackground=self.border_color)
            card.pack(fill="x", padx=20, pady=6)
            
            avatar_f = tk.Frame(card, bg="#f8fafc", width=40, height=40)
            avatar_f.pack(side="left", padx=(0, 15))
            avatar_f.pack_propagate(False)
            
            tk.Label(avatar_f, text="👤", font=("Segoe UI", 12), bg="#f8fafc").pack(expand=True)
            
            tk.Label(card, text=paciente.upper(), font=("Segoe UI", 10, "bold"), bg="white", fg=self.text_main).pack(side="left")
            
            badge_f = tk.Frame(card, bg="#f1f5f9", padx=12, pady=6)
            badge_f.pack(side="right")
            tk.Label(badge_f, text=f"{count} CONSULTAS", font=("Consolas", 9, "bold"), bg="#f1f5f9", fg="#16a34a").pack()

    def _h_report_edad_promedio(self):
        """Reporte 3: Edad promedio de pacientes por enfermedad (Modernizado)."""
        self._clear_viz()
        serie = self.analizador.edad_promedio_por_diagnostico()
        if isinstance(serie, str):
            self._mostrar_texto_simple(serie)
            return

        # Contenedor Principal Scrollable
        canvas_f = tk.Canvas(self.viz_area, bg="#f8fafc", highlightthickness=0)
        v_scroll = ttk.Scrollbar(self.viz_area, orient="vertical", command=canvas_f.yview, style="Modern.Vertical.TScrollbar")
        scroll_f = tk.Frame(canvas_f, bg="#f8fafc")
        
        scroll_f.bind("<Configure>", lambda e: canvas_f.configure(scrollregion=canvas_f.bbox("all")))
        canvas_f.create_window((0,0), window=scroll_f, anchor="nw")
        canvas_f.configure(yscrollcommand=v_scroll.set)
        
        canvas_f.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        
        canvas_f.bind_all("<MouseWheel>", lambda e: canvas_f.yview_scroll(int(-1*(e.delta/120)), "units"))

        # 1. ENCABEZADO Y TARJETAS TÉCNICAS
        header_f = tk.Frame(scroll_f, bg="#f8fafc", pady=20)
        header_f.pack(fill="x")
        tk.Label(header_f, text="🔬 REPORTE TÉCNICO: DISTRIBUCIÓN POR EDAD", font=("Segoe UI", 16, "bold"), bg="#f8fafc", fg=self.primary_color).pack()
        
        import textwrap
        serie_sorted = serie.sort_values(ascending=False)
        for enfermedad, edad in serie_sorted.items():
            # Evitar tarjetas en blanco si el diagnóstico está vacío
            if not enfermedad or str(enfermedad).strip() == "" or str(enfermedad).lower() == 'nan': 
                continue
                
            card = tk.Frame(scroll_f, bg="white", padx=20, pady=10, highlightthickness=1, highlightbackground=self.border_color)
            card.pack(fill="x", padx=40, pady=4)
            
            # Punto de color según riesgo de edad
            color = "#ef4444" if edad >= 55 else ("#f59e0b" if edad >= 35 else "#10b981")
            dot = tk.Frame(card, bg=color, width=10, height=10)
            dot.pack(side="left", padx=(0, 15))
            
            tk.Label(card, text=enfermedad.upper(), font=("Segoe UI", 10, "bold"), bg="white", fg=self.text_main).pack(side="left")
            
            badge_f = tk.Frame(card, bg="#f1f5f9", padx=10, pady=4)
            badge_f.pack(side="right")
            tk.Label(badge_f, text=f"{edad:.1f} AÑOS", font=("Consolas", 10, "bold"), bg="#f1f5f9", fg=self.text_main).pack()

        # 2. GRÁFICA (Integrada en el mismo scroll)
        tk.Label(scroll_f, text="VISUALIZACIÓN ANALÍTICA", font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg=self.text_dim).pack(pady=(40, 10))
        
        n_items = len(serie_sorted)
        chart_height = max(6, n_items * 0.5) 
        
        fig, ax = plt.subplots(figsize=(11, chart_height), dpi=100)
        fig.patch.set_facecolor('#f8fafc')
        serie_sorted.plot(kind="barh", ax=ax, color=self.secondary_color, edgecolor="white", width=0.7)
        
        ax.set_title("Edad Promedio por Diagnóstico", fontsize=12, fontweight='bold', pad=15)
        # Aplicamos wrapping también aquí para consistencia (Asegurando que sea string)
        labels = [textwrap.fill(str(l), width=25) for l in serie_sorted.index]
        ax.set_yticklabels(labels, fontsize=9, fontweight='500')
        ax.invert_yaxis()
        ax.set_facecolor('white')
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        
        plt.tight_layout()

        canvas_graph = FigureCanvasTkAgg(fig, master=scroll_f)
        canvas_graph.draw()
        canvas_graph.get_tk_widget().pack(fill="x", padx=40, pady=(0, 40))
        plt.close(fig)

    def _mostrar_texto_simple(self, texto):
        """Helper para mostrar un mensaje de texto plano en el área de visualización."""
        txt = tk.Text(self.viz_area, padx=25, pady=20, font=("Segoe UI", 11), bg="#f8fafc", relief="flat")
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", texto)
        txt.config(state="disabled")

    def _h_ia_preventiva(self):
        """Renderiza un panel de Inteligencia Clínica con tarjetas y visuales modernos."""
        self._clear_viz()
        
        container = tk.Frame(self.viz_area, bg="#f8fafc", padx=30, pady=30)
        container.pack(fill="both", expand=True)
        
        # Header del reporte
        header = tk.Frame(container, bg="#f8fafc")
        header.pack(fill="x", pady=(0, 30))
        
        tk.Label(header, text="✨ Inteligencia Clínica Proactiva", font=self.font_h2, 
                 bg="#f8fafc", fg=self.primary_color).pack(side="left")
        
        # Obtener datos
        df = self.analizador._preparar_dataset()
        res_preventivo = self.analizador.sugerir_chequeos_preventivos()
        res_ia = self.modelo_ia.analizar_sintomas_historicos(df['Sintomas']) if df is not None else []
        
        if not res_preventivo and not res_ia:
            tk.Label(container, text="No se han detectado patrones clínicos que requieran atención inmediata.", 
                     font=self.font_ui, bg="#f8fafc", fg=self.text_dim).pack(pady=50)
            return

        # Área de Scroll para las tarjetas
        canvas_f = tk.Canvas(container, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas_f.yview, style="Modern.Vertical.TScrollbar")
        scrollable_frame = tk.Frame(canvas_f, bg="#f8fafc")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_f.configure(scrollregion=canvas_f.bbox("all"))
        )

        canvas_f.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_f.configure(yscrollcommand=scrollbar.set)

        canvas_f.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Sección 1: Chequeos Sugeridos
        if res_preventivo:
            tk.Label(scrollable_frame, text="RECOMENDACIONES PREVENTIVAS", font=("Segoe UI", 9, "bold"),
                     bg="#f8fafc", fg=self.secondary_color).pack(anchor="w", pady=(0, 15))
            for item in res_preventivo:
                self._render_suggestion_card(scrollable_frame, item)

        # Sección 2: Patrones de Inteligencia Clínica (Ranking)
        if res_ia:
            tk.Label(scrollable_frame, text="SÍNTOMAS Y PATRONES DETECTADOS POR IA V3.0", font=("Segoe UI", 9, "bold"),
                     bg="#f8fafc", fg=self.accent_color).pack(anchor="w", pady=(30, 15))
            for item in res_ia:
                # El nuevo modelo ya devuelve los campos listos (titulo, detalle, icono, color)
                self._render_suggestion_card(scrollable_frame, item)

    def _render_suggestion_card(self, parent, data):
        """Dibuja una tarjeta de sugerencia clínica con estilo moderno."""
        card = tk.Frame(parent, bg="white", padx=20, pady=15,
                        highlightthickness=1, highlightbackground=self.border_color)
        card.pack(fill="x", pady=5)
        
        icon_f = tk.Frame(card, bg="#f1f5f9", width=40, height=40)
        icon_f.pack(side="left", padx=(0, 15))
        icon_f.pack_propagate(False)
        tk.Label(icon_f, text=data.get("icono", "✨"), font=("Segoe UI", 14), bg="#f1f5f9").pack(expand=True)
        
        info_f = tk.Frame(card, bg="white")
        info_f.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_f, text=data["titulo"], font=self.font_h3, bg="white", fg=self.text_main).pack(anchor="w")
        tk.Label(info_f, text=data["detalle"], font=self.font_body, bg="white", fg=self.text_dim).pack(anchor="w")
        
        # Badge de tipo
        badge_text = "IA SCAN" if "patron" in data else "PREVENTIVO"
        badge_color = self.accent_color if "patron" in data else self.secondary_color
        
        badge = tk.Label(card, text=badge_text, font=("Segoe UI", 7, "bold"), 
                         bg=badge_color, fg="white", padx=8, pady=2)
        badge.pack(side="right")

    def _clear_viz(self):
        # Desvincular eventos globales para evitar TclError al destruir el canvas
        self.unbind_all("<MouseWheel>")
        for w in self.viz_area.winfo_children(): w.destroy()

if __name__ == "__main__":
    app = BUAPMedicineApp()
    app.mainloop()
