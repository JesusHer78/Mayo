import re

class ModeloPreventivo:
    """
    ENGINE IA V3.0: Clinical Inference Engine (CIE)
    Sistema de inferencia médica basado en grafos de síntomas ponderados y 
    análisis de severidad probabilística.
    """
    
    def __init__(self):
        # Base de Conocimiento de Alta Densidad (Knowledge Base)
        # Formato: "Patología": {"Síntomas": {palabra: peso_relevancia}, "Gravedad": 1-10}
        self._knowledge_base = {
            "SÍNDROME CORONARIO AGUDO": {
                "sintomas": {"pecho": 10, "opresión": 9, "brazo izquierdo": 8, "mandíbula": 7, "sudor": 6, "náusea": 5, "disnea": 8, "infarto": 10},
                "gravedad": 10, "icono": "🫀", "color": "#dc2626", "rec": "Traslado inmediato a Cardiología / ECG Urgente."
            },
            "DIABETES MELLITUS T2": {
                "sintomas": {"sed": 9, "orina": 8, "polidipsia": 10, "hambre": 7, "visión borrosa": 8, "fatiga": 5, "glucosa": 9, "herida": 6},
                "gravedad": 7, "icono": "🧪", "color": "#4f46e5", "rec": "Perfil metabólico, Hemoglobina Glicosilada y fondo de ojo."
            },
            "ACCIDENTE CEREBROVASCULAR (ACV)": {
                "sintomas": {"cara": 9, "parálisis": 10, "hablar": 9, "confusión": 8, "equilibrio": 7, "vértigo": 6, "fuerza": 8, "asimetría": 10},
                "gravedad": 10, "icono": "🧠", "color": "#991b1b", "rec": "Activación de Código Ictus. Tomografía craneal urgente."
            },
            "INFECCIÓN RESPIRATORIA / NEUMONÍA": {
                "sintomas": {"tos": 8, "fiebre": 7, "flemas": 6, "respirar": 9, "escalofríos": 5, "pulmón": 7, "oxigeno": 8},
                "gravedad": 8, "icono": "🌬️", "color": "#0891b2", "rec": "Rayos X de Tórax, oximetría y cultivo de esputo."
            },
            "HIPERTENSIÓN ARTERIAL CRÍTICA": {
                "sintomas": {"nuca": 8, "oído": 7, "zumbido": 8, "presión": 9, "tensión": 9, "cefalea": 7, "fosfenos": 9},
                "gravedad": 9, "icono": "⚖️", "color": "#f59e0b", "rec": "Monitoreo de presión 24h (MAPA) y fondo de ojo."
            },
            "GASTROENTERITIS / ABDOMEN AGUDO": {
                "sintomas": {"estomago": 8, "diarrea": 7, "vómito": 8, "dolor agudo": 9, "apéndice": 10, "deshidratación": 8, "reflujo": 5},
                "gravedad": 7, "icono": "🤢", "color": "#059669", "rec": "Ecografía abdominal y pruebas de electrolitos."
            },
            "TRASTORNO ANSIOSO / PÁNICO": {
                "sintomas": {"ansiedad": 9, "pánico": 10, "palpitación": 8, "temblor": 6, "miedo": 7, "ahogo": 8, "insomnio": 5},
                "gravedad": 5, "icono": "🧘", "color": "#8b5cf6", "rec": "Evaluación psicológica y descarte orgánico cardiovascular."
            }
        }

        # Palabras de negación para evitar falsos positivos
        self._negations = ["no", "sin", "ningún", "nunca", "tampoco", "descartado"]

    def realizar_triage(self, texto_sintomas):
        """Analiza la entrada y calcula la severidad usando el motor de inferencia."""
        texto = texto_sintomas.lower()
        if not texto.strip():
            return {"nivel": "ESPERANDO", "color": "#94a3b8", "mensaje": "Inicie la entrada de datos clínicos..."}

        # Analizar severidad máxima detectada
        score_max = 0
        hallazgo_critico = None
        
        # Sistema de detección por pesos
        for patologia, info in self._knowledge_base.items():
            current_score = 0
            for sintoma, peso in info["sintomas"].items():
                # Búsqueda inteligente (Regex para evitar coincidencias parciales erróneas)
                if re.search(rf"\b{sintoma}\b", texto):
                    # Verificar negación cercana (lookbehind simplificado)
                    # Si hay un 'no' antes de la palabra, reducimos el peso drásticamente
                    contexto = texto.split(sintoma)[0].split()[-3:] # últimos 3 palabras antes
                    if any(neg in contexto for neg in self._negations):
                        continue 
                    current_score += peso
            
            if current_score > score_max:
                score_max = current_score
                hallazgo_critico = patologia

        # Clasificación Final del Triage
        if score_max >= 15: # Umbral crítico (Múltiples síntomas de alta gravedad)
            info = self._knowledge_base[hallazgo_critico]
            return {
                "nivel": "EMERGENCIA NIVEL 1",
                "color": info["color"],
                "mensaje": f"⚠️ ALTA PROBABILIDAD DE: {hallazgo_critico}. {info['rec']}"
            }
        elif score_max >= 8:
            info = self._knowledge_base[hallazgo_critico]
            return {
                "nivel": "PRIORIDAD NIVEL 2",
                "color": "#ea580c",
                "mensaje": f"🟠 SOSPECHA CLÍNICA: {hallazgo_critico}. Se sugiere {info['rec']}"
            }
        elif score_max >= 1:
            return {
                "nivel": "ESTABLE / NIVEL 3",
                "color": "#16a34a",
                "mensaje": "🟢 Sintomatología leve. Proceder con protocolo de consulta estándar."
            }
        
        return {"nivel": "NORMAL", "color": "#3b82f6", "mensaje": "No se detectan patrones de riesgo en la entrada actual."}

    def analizar_sintomas_historicos(self, series_sintomas):
        """
        Analiza el Big Data del paciente para detectar condiciones crónicas o evolutivas.
        Devuelve un ranking de sospechas diagnósticas por probabilidad.
        """
        if series_sintomas is None or series_sintomas.empty: return []
        
        texto_completo = " ".join(series_sintomas.tolist()).lower()
        predicciones = []

        for patologia, info in self._knowledge_base.items():
            puntos = 0
            coincidencias = []
            
            for sintoma, peso in info["sintomas"].items():
                if sintoma in texto_completo:
                    puntos += peso
                    coincidencias.append(sintoma)
            
            # Cálculo de "Confianza IA"
            total_posible = sum(info["sintomas"].values())
            confianza = (puntos / total_posible) * 100

            if confianza >= 25: # Umbral de reporte histórico
                predicciones.append({
                    "patron": ", ".join(coincidencias[:3]) + "...",
                    "titulo": f"Ranking IA: {patologia}",
                    "detalle": f"Confianza de detección: {confianza:.1f}%. Recomendación: {info['rec']}",
                    "icono": info["icono"],
                    "color": info["color"]
                })
        
        # Ordenar por nivel de confianza
        return sorted(predicciones, key=lambda x: float(x["detalle"].split(":")[1].split("%")[0]), reverse=True)
