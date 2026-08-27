import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os

class KSPHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("KSP Helper - Помощник пилота")
        self.root.geometry("850x750")
        self.root.resizable(True, True)
        
        self.version = "0.3.2"
        self.current_lang = "russian"
        
        # Загружаем настройки
        self.settings = {
            "theme": "blue",
            "language": "russian"
        }
        self.load_settings()
        self.current_lang = self.settings["language"]
        
        # Применяем тему
        self.apply_theme()
        
        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладки
        self.delta_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.delta_frame, text="🚀 Калькулятор ΔV")
        
        self.advisor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.advisor_frame, text="🛠️ Советник по сборке")
        
        self.orbit_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.orbit_frame, text="🛰️ Орбитальная механика")
        
        self.lander_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.lander_frame, text="🌙 Посадка/Взлёт")
        
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Настройки")
        
        # Инициализация
        self.init_delta_calculator()
        self.init_rocket_advisor()
        self.init_placeholder_tabs()
        self.init_settings_tab()
        
        # Версия
        self.version_label = ttk.Label(root, text=f"Версия {self.version}", 
                                      font=('Arial', 8, 'italic'))
        self.version_label.place(x=10, y=self.root.winfo_height() - 30)
        self.root.bind('<Configure>', self.update_version_position)
        
        # Применяем язык
        self.update_language()
    
    def get_text(self, key):
        """Получение перевода на текущем языке"""
        texts = {
            "russian": {
                "title": "KSP Helper - Помощник пилота",
                "calc_title": "Калькулятор ΔV",
                "advisor_title": "Советник по сборке ракеты",
                "orbit_title": "Орбитальная механика",
                "lander_title": "Посадка/Взлёт",
                "settings_title": "Настройки",
                "params": "Параметры ракеты",
                "mass_start": "Стартовая масса (т):",
                "mass_end": "Конечная масса (т):",
                "isp": "Удельный импульс Isp (с):",
                "gravity": "Гравитация (м/с²):",
                "stages": "Количество ступеней:",
                "quick_settings": "Быстрые настройки",
                "stage_params": "Параметры ступеней",
                "calc_btn": "Рассчитать ΔV",
                "results": "Результаты",
                "advice": "💡 Совет: Для Kerbin требуется ~3400 м/с ΔV",
                "stage": "Ступень",
                "mass_start_short": "Старт. масса:",
                "mass_end_short": "Конеч. масса:",
                "isp_short": "Isp:",
                "soon": "⏳ СКОРО БУДЕТ!",
                "settings": "Настройки",
                "language": "Язык",
                "theme": "Тема",
                "blue_theme": "Синяя",
                "light_theme": "Светлая",
                "apply": "Применить",
                "settings_saved": "Настройки сохраняются автоматически",
                "settings_applied": "Настройки применены!",
                "success": "Успех",
                "error": "Ошибка",
                "mass_error": "Ошибка в массе!",
                "isp_error": "Ошибка в Isp!",
                "value_error": "Введите корректные числа!",
                "results_title": "РЕЗУЛЬТАТЫ РАСЧЕТА",
                "body": "Небесное тело:",
                "gravity_val": "Гравитация:",
                "mass_ratio": "Массовое число:",
                "total_dv": "ИТОГОВАЯ ΔV:",
                "enough": "✅ ΔV достаточно",
                "not_enough": "⚠️ ΔV недостаточно",
                "missing": "Не хватает",
                "required": "Требуется:",
                "available": "Доступно:",
                "stock": "Запас:",
                "version": "Версия",
                "advisor_desc": "Выберите цель миссии и получите рекомендации по сборке ракеты",
                "mission_target": "Цель миссии:",
                "target_orbit": "Выход на орбиту",
                "target_landing": "Посадка",
                "target_interplanetary": "Межпланетный перелёт",
                "rocket_size": "Размер ракеты:",
                "size_small": "Маленькая (до 5т)",
                "size_medium": "Средняя (5-20т)",
                "size_large": "Большая (20-50т)",
                "size_heavy": "Тяжёлая (50т+)",
                "get_advice": "Получить совет",
                "engine_types": "Рекомендуемые двигатели:",
                "stages_count": "Рекомендуемое количество ступеней:",
                "fuel_types": "Рекомендуемое топливо:",
                "tips": "Советы:",
                "no_advice": "Выберите параметры и нажмите 'Получить совет'",
                "total_dv_text": "Общая ΔV"
            },
            "english": {
                "title": "KSP Helper - Pilot Assistant",
                "calc_title": "ΔV Calculator",
                "advisor_title": "Rocket Building Advisor",
                "orbit_title": "Orbital Mechanics",
                "lander_title": "Landing/Takeoff",
                "settings_title": "Settings",
                "params": "Rocket Parameters",
                "mass_start": "Launch mass (t):",
                "mass_end": "Final mass (t):",
                "isp": "Specific impulse Isp (s):",
                "gravity": "Gravity (m/s²):",
                "stages": "Number of stages:",
                "quick_settings": "Quick settings",
                "stage_params": "Stage parameters",
                "calc_btn": "Calculate ΔV",
                "results": "Results",
                "advice": "💡 Tip: Kerbin orbit requires ~3400 m/s ΔV",
                "stage": "Stage",
                "mass_start_short": "Launch mass:",
                "mass_end_short": "Final mass:",
                "isp_short": "Isp:",
                "soon": "⏳ COMING SOON!",
                "settings": "Settings",
                "language": "Language",
                "theme": "Theme",
                "blue_theme": "Blue",
                "light_theme": "Light",
                "apply": "Apply",
                "settings_saved": "Settings are saved automatically",
                "settings_applied": "Settings applied!",
                "success": "Success",
                "error": "Error",
                "mass_error": "Mass error!",
                "isp_error": "Isp error!",
                "value_error": "Enter valid numbers!",
                "results_title": "CALCULATION RESULTS",
                "body": "Celestial body:",
                "gravity_val": "Gravity:",
                "mass_ratio": "Mass ratio:",
                "total_dv": "TOTAL ΔV:",
                "enough": "✅ ΔV is sufficient",
                "not_enough": "⚠️ ΔV is insufficient",
                "missing": "Missing",
                "required": "Required:",
                "available": "Available:",
                "stock": "Stock:",
                "version": "Version",
                "advisor_desc": "Select mission goal and get rocket building recommendations",
                "mission_target": "Mission target:",
                "target_orbit": "Orbit",
                "target_landing": "Landing",
                "target_interplanetary": "Interplanetary",
                "rocket_size": "Rocket size:",
                "size_small": "Small (up to 5t)",
                "size_medium": "Medium (5-20t)",
                "size_large": "Large (20-50t)",
                "size_heavy": "Heavy (50t+)",
                "get_advice": "Get advice",
                "engine_types": "Recommended engines:",
                "stages_count": "Recommended stages:",
                "fuel_types": "Recommended fuel:",
                "tips": "Tips:",
                "no_advice": "Select parameters and click 'Get advice'",
                "total_dv_text": "Total ΔV"
            },
            "german": {
                "title": "KSP Helfer - Pilotenassistent",
                "calc_title": "ΔV-Rechner",
                "advisor_title": "Raketenbau-Berater",
                "orbit_title": "Orbitalmechanik",
                "lander_title": "Landung/Start",
                "settings_title": "Einstellungen",
                "params": "Raketenparameter",
                "mass_start": "Startmasse (t):",
                "mass_end": "Endmasse (t):",
                "isp": "Spezifischer Impuls Isp (s):",
                "gravity": "Schwerkraft (m/s²):",
                "stages": "Anzahl Stufen:",
                "quick_settings": "Schnelleinstellungen",
                "stage_params": "Stufenparameter",
                "calc_btn": "ΔV berechnen",
                "results": "Ergebnisse",
                "advice": "💡 Tipp: Kerbin-Orbit benötigt ~3400 m/s ΔV",
                "stage": "Stufe",
                "mass_start_short": "Startmasse:",
                "mass_end_short": "Endmasse:",
                "isp_short": "Isp:",
                "soon": "⏳ BALD VERFÜGBAR!",
                "settings": "Einstellungen",
                "language": "Sprache",
                "theme": "Thema",
                "blue_theme": "Blau",
                "light_theme": "Hell",
                "apply": "Anwenden",
                "settings_saved": "Einstellungen werden automatisch gespeichert",
                "settings_applied": "Einstellungen übernommen!",
                "success": "Erfolg",
                "error": "Fehler",
                "mass_error": "Massenfehler!",
                "isp_error": "Isp-Fehler!",
                "value_error": "Gültige Zahlen eingeben!",
                "results_title": "BERECHNUNGSERGEBNISSE",
                "body": "Himmelskörper:",
                "gravity_val": "Schwerkraft:",
                "mass_ratio": "Massenverhältnis:",
                "total_dv": "GESAMT-ΔV:",
                "enough": "✅ ΔV ausreichend",
                "not_enough": "⚠️ ΔV unzureichend",
                "missing": "Fehlend",
                "required": "Erforderlich:",
                "available": "Verfügbar:",
                "stock": "Reserve:",
                "version": "Version",
                "advisor_desc": "Wählen Sie Missionsziel und erhalten Sie Bauempfehlungen",
                "mission_target": "Missionsziel:",
                "target_orbit": "Orbit",
                "target_landing": "Landung",
                "target_interplanetary": "Interplanetar",
                "rocket_size": "Raketengröße:",
                "size_small": "Klein (bis 5t)",
                "size_medium": "Mittel (5-20t)",
                "size_large": "Groß (20-50t)",
                "size_heavy": "Schwer (50t+)",
                "get_advice": "Beratung erhalten",
                "engine_types": "Empfohlene Triebwerke:",
                "stages_count": "Empfohlene Stufen:",
                "fuel_types": "Empfohlener Treibstoff:",
                "tips": "Tipps:",
                "no_advice": "Wählen Sie Parameter und klicken Sie 'Beratung erhalten'",
                "total_dv_text": "Gesamt-ΔV"
            },
            "portuguese": {
                "title": "KSP Helper - Assistente de Piloto",
                "calc_title": "Calculadora ΔV",
                "advisor_title": "Consultor de Montagem",
                "orbit_title": "Mecânica Orbital",
                "lander_title": "Pousagem/Decolagem",
                "settings_title": "Configurações",
                "params": "Parâmetros do Foguete",
                "mass_start": "Massa de lançamento (t):",
                "mass_end": "Massa final (t):",
                "isp": "Impulso específico Isp (s):",
                "gravity": "Gravidade (m/s²):",
                "stages": "Número de estágios:",
                "quick_settings": "Configurações rápidas",
                "stage_params": "Parâmetros dos estágios",
                "calc_btn": "Calcular ΔV",
                "results": "Resultados",
                "advice": "💡 Dica: Órbita de Kerbin requer ~3400 m/s ΔV",
                "stage": "Estágio",
                "mass_start_short": "Massa inicial:",
                "mass_end_short": "Massa final:",
                "isp_short": "Isp:",
                "soon": "⏳ EM BREVE!",
                "settings": "Configurações",
                "language": "Idioma",
                "theme": "Tema",
                "blue_theme": "Azul",
                "light_theme": "Claro",
                "apply": "Aplicar",
                "settings_saved": "Configurações salvas automaticamente",
                "settings_applied": "Configurações aplicadas!",
                "success": "Sucesso",
                "error": "Erro",
                "mass_error": "Erro de massa!",
                "isp_error": "Erro de Isp!",
                "value_error": "Digite números válidos!",
                "results_title": "RESULTADOS DO CÁLCULO",
                "body": "Corpo celeste:",
                "gravity_val": "Gravidade:",
                "mass_ratio": "Razão de massa:",
                "total_dv": "ΔV TOTAL:",
                "enough": "✅ ΔV suficiente",
                "not_enough": "⚠️ ΔV insuficiente",
                "missing": "Faltando",
                "required": "Necessário:",
                "available": "Disponível:",
                "stock": "Estoque:",
                "version": "Versão",
                "advisor_desc": "Selecione o objetivo da missão e obtenha recomendações",
                "mission_target": "Objetivo da missão:",
                "target_orbit": "Órbita",
                "target_landing": "Pousagem",
                "target_interplanetary": "Interplanetário",
                "rocket_size": "Tamanho do foguete:",
                "size_small": "Pequeno (até 5t)",
                "size_medium": "Médio (5-20t)",
                "size_large": "Grande (20-50t)",
                "size_heavy": "Pesado (50t+)",
                "get_advice": "Obter conselho",
                "engine_types": "Motores recomendados:",
                "stages_count": "Estágios recomendados:",
                "fuel_types": "Combustível recomendado:",
                "tips": "Dicas:",
                "no_advice": "Selecione parâmetros e clique em 'Obter conselho'",
                "total_dv_text": "ΔV Total"
            },
            "spanish": {
                "title": "KSP Helper - Asistente de Piloto",
                "calc_title": "Calculadora ΔV",
                "advisor_title": "Asesor de Construcción",
                "orbit_title": "Mecánica Orbital",
                "lander_title": "Aterrizaje/Despegue",
                "settings_title": "Configuración",
                "params": "Parámetros del Cohete",
                "mass_start": "Masa de lanzamiento (t):",
                "mass_end": "Masa final (t):",
                "isp": "Impulso específico Isp (s):",
                "gravity": "Gravedad (m/s²):",
                "stages": "Número de etapas:",
                "quick_settings": "Configuración rápida",
                "stage_params": "Parámetros de etapas",
                "calc_btn": "Calcular ΔV",
                "results": "Resultados",
                "advice": "💡 Consejo: Órbita de Kerbin requiere ~3400 m/s ΔV",
                "stage": "Etapa",
                "mass_start_short": "Masa inicial:",
                "mass_end_short": "Masa final:",
                "isp_short": "Isp:",
                "soon": "⏳ ¡PRÓXIMAMENTE!",
                "settings": "Configuración",
                "language": "Idioma",
                "theme": "Tema",
                "blue_theme": "Azul",
                "light_theme": "Claro",
                "apply": "Aplicar",
                "settings_saved": "La configuración se guarda automáticamente",
                "settings_applied": "¡Configuración aplicada!",
                "success": "Éxito",
                "error": "Error",
                "mass_error": "¡Error de masa!",
                "isp_error": "¡Error de Isp!",
                "value_error": "¡Ingrese números válidos!",
                "results_title": "RESULTADOS DEL CÁLCULO",
                "body": "Cuerpo celeste:",
                "gravity_val": "Gravedad:",
                "mass_ratio": "Relación de masas:",
                "total_dv": "ΔV TOTAL:",
                "enough": "✅ ΔV suficiente",
                "not_enough": "⚠️ ΔV insuficiente",
                "missing": "Faltante",
                "required": "Requerido:",
                "available": "Disponible:",
                "stock": "Reserva:",
                "version": "Versión",
                "advisor_desc": "Seleccione el objetivo de la misión y obtenga recomendaciones",
                "mission_target": "Objetivo de la misión:",
                "target_orbit": "Órbita",
                "target_landing": "Aterrizaje",
                "target_interplanetary": "Interplanetario",
                "rocket_size": "Tamaño del cohete:",
                "size_small": "Pequeño (hasta 5t)",
                "size_medium": "Mediano (5-20t)",
                "size_large": "Grande (20-50t)",
                "size_heavy": "Pesado (50t+)",
                "get_advice": "Obtener consejo",
                "engine_types": "Motores recomendados:",
                "stages_count": "Etapas recomendadas:",
                "fuel_types": "Combustible recomendado:",
                "tips": "Consejos:",
                "no_advice": "Seleccione parámetros y haga clic en 'Obtener consejo'",
                "total_dv_text": "ΔV Total"
            },
            "french": {
                "title": "KSP Helper - Assistant Pilote",
                "calc_title": "Calculateur ΔV",
                "advisor_title": "Conseiller de Construction",
                "orbit_title": "Mécanique Orbitale",
                "lander_title": "Atterrissage/Décollage",
                "settings_title": "Paramètres",
                "params": "Paramètres de la Fusée",
                "mass_start": "Masse de lancement (t):",
                "mass_end": "Masse finale (t):",
                "isp": "Impulsion spécifique Isp (s):",
                "gravity": "Gravité (m/s²):",
                "stages": "Nombre d'étages:",
                "quick_settings": "Réglages rapides",
                "stage_params": "Paramètres des étages",
                "calc_btn": "Calculer ΔV",
                "results": "Résultats",
                "advice": "💡 Conseil: L'orbite de Kerbin nécessite ~3400 m/s ΔV",
                "stage": "Étage",
                "mass_start_short": "Masse initiale:",
                "mass_end_short": "Masse finale:",
                "isp_short": "Isp:",
                "soon": "⏳ BIENTÔT!",
                "settings": "Paramètres",
                "language": "Langue",
                "theme": "Thème",
                "blue_theme": "Bleu",
                "light_theme": "Clair",
                "apply": "Appliquer",
                "settings_saved": "Les paramètres sont sauvegardés automatiquement",
                "settings_applied": "Paramètres appliqués!",
                "success": "Succès",
                "error": "Erreur",
                "mass_error": "Erreur de masse!",
                "isp_error": "Erreur d'Isp!",
                "value_error": "Entrez des nombres valides!",
                "results_title": "RÉSULTATS DU CALCUL",
                "body": "Corps céleste:",
                "gravity_val": "Gravité:",
                "mass_ratio": "Rapport de masse:",
                "total_dv": "ΔV TOTAL:",
                "enough": "✅ ΔV suffisant",
                "not_enough": "⚠️ ΔV insuffisant",
                "missing": "Manquant",
                "required": "Requis:",
                "available": "Disponible:",
                "stock": "Réserve:",
                "version": "Version",
                "advisor_desc": "Choisissez l'objectif de la mission et obtenez des recommandations",
                "mission_target": "Objectif de la mission:",
                "target_orbit": "Orbite",
                "target_landing": "Atterrissage",
                "target_interplanetary": "Interplanétaire",
                "rocket_size": "Taille de la fusée:",
                "size_small": "Petite (jusqu'à 5t)",
                "size_medium": "Moyenne (5-20t)",
                "size_large": "Grande (20-50t)",
                "size_heavy": "Lourde (50t+)",
                "get_advice": "Obtenir un conseil",
                "engine_types": "Moteurs recommandés:",
                "stages_count": "Étages recommandés:",
                "fuel_types": "Carburant recommandé:",
                "tips": "Conseils:",
                "no_advice": "Sélectionnez les paramètres et cliquez sur 'Obtenir un conseil'",
                "total_dv_text": "ΔV Total"
            },
            "italian": {
                "title": "KSP Helper - Assistente Pilota",
                "calc_title": "Calcolatore ΔV",
                "advisor_title": "Consulente di Costruzione",
                "orbit_title": "Meccanica Orbitale",
                "lander_title": "Atterraggio/Decollo",
                "settings_title": "Impostazioni",
                "params": "Parametri del Razzo",
                "mass_start": "Massa di lancio (t):",
                "mass_end": "Massa finale (t):",
                "isp": "Impulso specifico Isp (s):",
                "gravity": "Gravità (m/s²):",
                "stages": "Numero di stadi:",
                "quick_settings": "Impostazioni rapide",
                "stage_params": "Parametri degli stadi",
                "calc_btn": "Calcola ΔV",
                "results": "Risultati",
                "advice": "💡 Consiglio: L'orbita di Kerbin richiede ~3400 m/s ΔV",
                "stage": "stadio",
                "mass_start_short": "Massa iniziale:",
                "mass_end_short": "Massa finale:",
                "isp_short": "Isp:",
                "soon": "⏳ PROSSIMAMENTE!",
                "settings": "Impostazioni",
                "language": "Lingua",
                "theme": "Tema",
                "blue_theme": "Blu",
                "light_theme": "Chiaro",
                "apply": "Applica",
                "settings_saved": "Le impostazioni vengono salvate automaticamente",
                "settings_applied": "Impostazioni applicate!",
                "success": "Successo",
                "error": "Errore",
                "mass_error": "Errore di massa!",
                "isp_error": "Errore di Isp!",
                "value_error": "Inserisci numeri validi!",
                "results_title": "RISULTATI DEL CALCOLO",
                "body": "Corpo celeste:",
                "gravity_val": "Gravità:",
                "mass_ratio": "Rapporto di massa:",
                "total_dv": "ΔV TOTALE:",
                "enough": "✅ ΔV sufficiente",
                "not_enough": "⚠️ ΔV insufficiente",
                "missing": "Mancante",
                "required": "Richiesto:",
                "available": "Disponibile:",
                "stock": "Riserva:",
                "version": "Versione",
                "advisor_desc": "Seleziona l'obiettivo della missione e ottieni raccomandazioni",
                "mission_target": "Obiettivo della missione:",
                "target_orbit": "Orbita",
                "target_landing": "Atterraggio",
                "target_interplanetary": "Interplanetario",
                "rocket_size": "Dimensioni del razzo:",
                "size_small": "Piccolo (fino a 5t)",
                "size_medium": "Medio (5-20t)",
                "size_large": "Grande (20-50t)",
                "size_heavy": "Pesante (50t+)",
                "get_advice": "Ottieni consiglio",
                "engine_types": "Motori raccomandati:",
                "stages_count": "Stadi raccomandati:",
                "fuel_types": "Carburante raccomandato:",
                "tips": "Consigli:",
                "no_advice": "Seleziona i parametri e clicca su 'Ottieni consiglio'",
                "total_dv_text": "ΔV Totale"
            }
        }
        
        lang = self.current_lang if self.current_lang in texts else "russian"
        return texts[lang].get(key, key)
    
    def update_language(self):
        """Обновление всего интерфейса"""
        # Заголовок окна
        self.root.title(self.get_text("title"))
        
        # Вкладки
        self.notebook.tab(0, text="🚀 " + self.get_text("calc_title"))
        self.notebook.tab(1, text="🛠️ " + self.get_text("advisor_title"))
        self.notebook.tab(2, text="🛰️ " + self.get_text("orbit_title"))
        self.notebook.tab(3, text="🌙 " + self.get_text("lander_title"))
        self.notebook.tab(4, text="⚙️ " + self.get_text("settings_title"))
        
        # Версия
        self.version_label.config(text=f"{self.get_text('version')} {self.version}")
        
        # Обновляем все виджеты
        self.update_all_widgets()
    
    def update_all_widgets(self):
        """Обновление всех виджетов в приложении"""
        # Калькулятор
        for widget in self.delta_frame.winfo_children():
            self.update_widget_text(widget)
        
        # Советник
        for widget in self.advisor_frame.winfo_children():
            self.update_widget_text(widget)
        
        # Заглушки
        self.update_placeholders()
        
        # Настройки
        for widget in self.settings_frame.winfo_children():
            self.update_widget_text(widget)
    
    def update_widget_text(self, widget):
        """Рекурсивное обновление текста виджетов"""
        # Обновляем Label
        if isinstance(widget, ttk.Label):
            current = widget.cget("text")
            # Проверяем ключи по содержимому
            if "Стартовая масса" in current or "Launch mass" in current or "Startmasse" in current:
                widget.config(text=self.get_text("mass_start"))
            elif "Конечная масса" in current or "Final mass" in current or "Endmasse" in current:
                widget.config(text=self.get_text("mass_end"))
            elif "Удельный импульс" in current or "Specific impulse" in current or "Spezifischer" in current:
                widget.config(text=self.get_text("isp"))
            elif "Гравитация" in current or "Gravity" in current or "Schwerkraft" in current:
                widget.config(text=self.get_text("gravity"))
            elif "Количество ступеней" in current or "Number of stages" in current or "Anzahl" in current:
                widget.config(text=self.get_text("stages"))
            elif "Быстрые настройки" in current or "Quick settings" in current:
                widget.config(text=self.get_text("quick_settings"))
            elif "Совет" in current or "Tip" in current or "Tipp" in current:
                widget.config(text=self.get_text("advice"))
            elif "Параметры ракеты" in current or "Rocket Parameters" in current:
                widget.config(text=self.get_text("params"))
            elif "Параметры ступеней" in current or "Stage parameters" in current:
                widget.config(text=self.get_text("stage_params"))
            elif "Результаты" in current or "Results" in current or "Ergebnisse" in current:
                widget.config(text=self.get_text("results"))
            elif "Цель миссии" in current or "Mission target" in current:
                widget.config(text=self.get_text("mission_target"))
            elif "Размер ракеты" in current or "Rocket size" in current:
                widget.config(text=self.get_text("rocket_size"))
            elif "Рекомендуемые двигатели" in current or "Recommended engines" in current:
                widget.config(text=self.get_text("engine_types"))
            elif "Рекомендуемое топливо" in current or "Recommended fuel" in current:
                widget.config(text=self.get_text("fuel_types"))
            elif "Советы" in current or "Tips" in current:
                widget.config(text=self.get_text("tips"))
            elif "Выберите цель" in current or "Select mission" in current:
                widget.config(text=self.get_text("advisor_desc"))
        
        # Обновляем кнопки
        elif isinstance(widget, ttk.Button):
            current = widget.cget("text")
            if "Рассчитать" in current or "Calculate" in current or "berechnen" in current:
                widget.config(text=self.get_text("calc_btn"))
            elif "Получить совет" in current or "Get advice" in current:
                widget.config(text=self.get_text("get_advice"))
            elif "Применить" in current or "Apply" in current:
                widget.config(text=self.get_text("apply"))
        
        # Обновляем LabelFrame
        elif isinstance(widget, ttk.LabelFrame):
            current = widget.cget("text")
            if "Параметры ракеты" in current or "Rocket Parameters" in current:
                widget.config(text=self.get_text("params"))
            elif "Параметры ступеней" in current or "Stage parameters" in current:
                widget.config(text=self.get_text("stage_params"))
            elif "Результаты" in current or "Results" in current:
                widget.config(text=self.get_text("results"))
            elif "Язык" in current or "Language" in current or "Sprache" in current:
                widget.config(text=self.get_text("language"))
            elif "Тема" in current or "Theme" in current or "Thema" in current:
                widget.config(text=self.get_text("theme"))
        
        # Обновляем Combobox
        elif isinstance(widget, ttk.Combobox):
            current_values = widget.cget("values")
            if current_values:
                # Обновляем значения в комбобоксах
                new_values = []
                for val in current_values:
                    if "орбит" in val or "Orbit" in val:
                        new_values.append(self.get_text("target_orbit"))
                    elif "посадк" in val or "Landing" in val:
                        new_values.append(self.get_text("target_landing"))
                    elif "межпланет" in val or "Interplanetary" in val:
                        new_values.append(self.get_text("target_interplanetary"))
                    elif "маленьк" in val or "Small" in val:
                        new_values.append(self.get_text("size_small"))
                    elif "средн" in val or "Medium" in val:
                        new_values.append(self.get_text("size_medium"))
                    elif "больш" in val or "Large" in val:
                        new_values.append(self.get_text("size_large"))
                    elif "тяжёл" in val or "Heavy" in val:
                        new_values.append(self.get_text("size_heavy"))
                    else:
                        new_values.append(val)
                if new_values:
                    widget['values'] = new_values
                    # Обновляем текущее значение если оно изменилось
                    current = widget.get()
                    if current in current_values:
                        idx = current_values.index(current)
                        if idx < len(new_values):
                            widget.set(new_values[idx])
        
        # Рекурсивно обходим дочерние виджеты
        for child in widget.winfo_children():
            self.update_widget_text(child)
    
    def update_placeholders(self):
        """Обновление заглушек"""
        for widget in self.orbit_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.config(text="🛰️ " + self.get_text("orbit_title").upper() + 
                             "\n\n• Расчёт орбитальных параметров\n• Скорость на орбите\n• Период обращения\n• Гомановский переход\n\n" + 
                             self.get_text("soon"))
        
        for widget in self.lander_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.config(text="🌙 " + self.get_text("lander_title").upper() + 
                             "\n\n• Расчёт ΔV для посадки\n• Оптимальная траектория\n• Вертикальная скорость\n• Мягкая посадка\n\n" + 
                             self.get_text("soon"))
    
    def load_settings(self):
        try:
            if os.path.exists("ksp_settings.json"):
                with open("ksp_settings.json", "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
        except:
            pass
    
    def save_settings(self):
        try:
            with open("ksp_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def apply_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        if self.settings["theme"] == "blue":
            self.root.configure(bg='#1a2a4a')
            style.configure('TFrame', background='#1a2a4a')
            style.configure('TLabel', background='#1a2a4a', foreground='white')
            style.configure('TLabelframe', background='#1a2a4a', foreground='white')
            style.configure('TLabelframe.Label', background='#1a2a4a', foreground='white')
            style.configure('TButton', background='#2a4a7a', foreground='white')
            style.map('TButton', background=[('active', '#3a5a8a')])
            style.configure('TEntry', fieldbackground='#2a3a5a', foreground='white')
            style.configure('TCombobox', fieldbackground='#2a3a5a', foreground='white')
            style.configure('TSpinbox', fieldbackground='#2a3a5a', foreground='white')
            style.configure('TNotebook', background='#1a2a4a')
            style.configure('TNotebook.Tab', background='#2a4a7a', foreground='white')
            style.map('TNotebook.Tab', background=[('selected', '#3a5a9a')])
            style.configure('TRadiobutton', background='#1a2a4a', foreground='white')
            self.text_bg = '#2a3a5a'
            self.text_fg = 'white'
        else:
            self.root.configure(bg='#f0f0f0')
            style.configure('TFrame', background='#f0f0f0')
            style.configure('TLabel', background='#f0f0f0', foreground='black')
            style.configure('TLabelframe', background='#f0f0f0', foreground='black')
            style.configure('TLabelframe.Label', background='#f0f0f0', foreground='black')
            style.configure('TButton', background='#e0e0e0', foreground='black')
            style.map('TButton', background=[('active', '#d0d0d0')])
            style.configure('TEntry', fieldbackground='white', foreground='black')
            style.configure('TCombobox', fieldbackground='white', foreground='black')
            style.configure('TSpinbox', fieldbackground='white', foreground='black')
            style.configure('TNotebook', background='#f0f0f0')
            style.configure('TNotebook.Tab', background='#e0e0e0', foreground='black')
            style.map('TNotebook.Tab', background=[('selected', '#ffffff')])
            style.configure('TRadiobutton', background='#f0f0f0', foreground='black')
            self.text_bg = 'white'
            self.text_fg = 'black'
        
        if hasattr(self, 'result_text'):
            self.result_text.configure(bg=self.text_bg, fg=self.text_fg)
        if hasattr(self, 'advice_text'):
            self.advice_text.configure(bg=self.text_bg, fg=self.text_fg)
    
    def update_version_position(self, event=None):
        self.version_label.place(x=10, y=self.root.winfo_height() - 30)
    
    def init_settings_tab(self):
        settings_frame = ttk.Frame(self.settings_frame, padding="20")
        settings_frame.pack(fill='both', expand=True)
        
        title = ttk.Label(settings_frame, text="⚙️ " + self.get_text("settings_title"), 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 30))
        
        lang_frame = ttk.LabelFrame(settings_frame, text=self.get_text("language"), padding="15")
        lang_frame.pack(fill='x', pady=(0, 15))
        
        self.lang_var = tk.StringVar(value=self.settings["language"])
        
        languages = [
            ("Русский", "russian"),
            ("English", "english"),
            ("Deutsch", "german"),
            ("Português", "portuguese"),
            ("Español", "spanish"),
            ("Français", "french"),
            ("Italiano", "italian")
        ]
        
        for lang_name, lang_code in languages:
            ttk.Radiobutton(lang_frame, text=lang_name, variable=self.lang_var, 
                           value=lang_code, command=self.change_language).pack(anchor='w', pady=2)
        
        theme_frame = ttk.LabelFrame(settings_frame, text=self.get_text("theme"), padding="15")
        theme_frame.pack(fill='x', pady=(0, 15))
        
        self.theme_var = tk.StringVar(value=self.settings["theme"])
        
        ttk.Radiobutton(theme_frame, text="🔵 " + self.get_text("blue_theme"), variable=self.theme_var, 
                       value="blue", command=self.change_theme).pack(anchor='w', pady=2)
        ttk.Radiobutton(theme_frame, text="⚪ " + self.get_text("light_theme"), variable=self.theme_var, 
                       value="light", command=self.change_theme).pack(anchor='w', pady=2)
        
        apply_btn = ttk.Button(settings_frame, text=self.get_text("apply"), 
                              command=self.apply_settings)
        apply_btn.pack(pady=20)
        
        info_label = ttk.Label(settings_frame, text=self.get_text("settings_saved"),
                              font=('Arial', 9, 'italic'))
        info_label.pack(pady=(10, 0))
    
    def change_language(self):
        self.settings["language"] = self.lang_var.get()
        self.current_lang = self.settings["language"]
        self.save_settings()
        self.update_language()
    
    def change_theme(self):
        self.settings["theme"] = self.theme_var.get()
        self.apply_theme()
        if hasattr(self, 'result_text'):
            self.result_text.configure(bg=self.text_bg, fg=self.text_fg)
        if hasattr(self, 'advice_text'):
            self.advice_text.configure(bg=self.text_bg, fg=self.text_fg)
        self.save_settings()
    
    def apply_settings(self):
        self.settings["language"] = self.lang_var.get()
        self.settings["theme"] = self.theme_var.get()
        self.current_lang = self.settings["language"]
        self.apply_theme()
        self.update_language()
        if hasattr(self, 'result_text'):
            self.result_text.configure(bg=self.text_bg, fg=self.text_fg)
        if hasattr(self, 'advice_text'):
            self.advice_text.configure(bg=self.text_bg, fg=self.text_fg)
        self.save_settings()
        messagebox.showinfo(self.get_text("success"), self.get_text("settings_applied"))
    
    def init_delta_calculator(self):
        main_canvas = tk.Canvas(self.delta_frame, bg=self.text_bg if hasattr(self, 'text_bg') else '#2a3a5a')
        scrollbar = ttk.Scrollbar(self.delta_frame, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        title = ttk.Label(scrollable_frame, text="🚀 " + self.get_text("calc_title"), 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 20))
        
        params_frame = ttk.LabelFrame(scrollable_frame, text=self.get_text("params"), padding="10")
        params_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(params_frame, text=self.get_text("mass_start")).grid(row=0, column=0, sticky='w', pady=5)
        self.mass_start = ttk.Entry(params_frame, width=15)
        self.mass_start.grid(row=0, column=1, pady=5, padx=(0, 20))
        self.mass_start.insert(0, "10.0")
        
        ttk.Label(params_frame, text=self.get_text("mass_end")).grid(row=0, column=2, sticky='w', pady=5)
        self.mass_end = ttk.Entry(params_frame, width=15)
        self.mass_end.grid(row=0, column=3, pady=5)
        self.mass_end.insert(0, "5.0")
        
        ttk.Label(params_frame, text=self.get_text("isp")).grid(row=1, column=0, sticky='w', pady=5)
        self.isp = ttk.Entry(params_frame, width=15)
        self.isp.grid(row=1, column=1, pady=5, padx=(0, 20))
        self.isp.insert(0, "320")
        
        ttk.Label(params_frame, text=self.get_text("gravity")).grid(row=1, column=2, sticky='w', pady=5)
        self.gravity = ttk.Combobox(params_frame, values=["9.81 (Kerbin)", "1.63 (Mun)", "3.71 (Duna)"], width=20)
        self.gravity.grid(row=1, column=3, pady=5)
        self.gravity.set("9.81 (Kerbin)")
        
        ttk.Label(params_frame, text=self.get_text("stages")).grid(row=2, column=0, sticky='w', pady=5)
        self.stages = ttk.Spinbox(params_frame, from_=1, to=5, width=13)
        self.stages.grid(row=2, column=1, pady=5, padx=(0, 20))
        self.stages.set(1)
        self.stages.bind('<<KeyRelease>>', self.update_stages)
        
        quick_frame = ttk.Frame(params_frame)
        quick_frame.grid(row=2, column=2, columnspan=2, pady=5, sticky='e')
        ttk.Label(quick_frame, text=self.get_text("quick_settings") + ":").pack(side='left', padx=(0, 5))
        ttk.Button(quick_frame, text="Kerbin", width=8, 
                  command=lambda: self.quick_setup(3400, "9.81 (Kerbin)")).pack(side='left', padx=2)
        ttk.Button(quick_frame, text="Mun", width=8,
                  command=lambda: self.quick_setup(580, "1.63 (Mun)")).pack(side='left', padx=2)
        ttk.Button(quick_frame, text="Duna", width=8,
                  command=lambda: self.quick_setup(1500, "3.71 (Duna)")).pack(side='left', padx=2)
        
        self.stages_frame = ttk.LabelFrame(scrollable_frame, text=self.get_text("stage_params"), padding="10")
        self.stages_frame.pack(fill='x', pady=(0, 10))
        self.stage_entries = []
        self.create_stage_inputs(1)
        
        calc_btn = ttk.Button(scrollable_frame, text=self.get_text("calc_btn"), command=self.calculate_delta_v)
        calc_btn.pack(pady=10)
        
        result_frame = ttk.LabelFrame(scrollable_frame, text=self.get_text("results"), padding="10")
        result_frame.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(result_frame, height=10, width=70, font=('Courier', 10),
                                  bg=self.text_bg if hasattr(self, 'text_bg') else '#2a3a5a',
                                  fg=self.text_fg if hasattr(self, 'text_fg') else 'white')
        self.result_text.pack(fill='both', expand=True)
        
        info_label = ttk.Label(scrollable_frame, text=self.get_text("advice"), font=('Arial', 9, 'italic'))
        info_label.pack(pady=(10, 0))
    
    def quick_setup(self, target_dv, gravity_value):
        self.gravity.set(gravity_value)
        isp = float(self.isp.get()) if self.isp.get() else 320
        mass_start = 10.0
        mass_ratio = math.exp(target_dv / (isp * 9.81))
        mass_end = mass_start / mass_ratio
        if mass_end > 0:
            self.mass_start.delete(0, tk.END)
            self.mass_start.insert(0, f"{mass_start:.2f}")
            self.mass_end.delete(0, tk.END)
            self.mass_end.insert(0, f"{mass_end:.2f}")
    
    def create_stage_inputs(self, num_stages):
        for widget in self.stages_frame.winfo_children():
            widget.destroy()
        self.stage_entries = []
        for i in range(num_stages):
            stage_frame = ttk.Frame(self.stages_frame)
            stage_frame.pack(fill='x', pady=5)
            ttk.Label(stage_frame, text=f"{self.get_text('stage')} {i+1}:", font=('Arial', 10, 'bold')).pack(side='left', padx=(0, 15))
            ttk.Label(stage_frame, text=self.get_text("mass_start_short")).pack(side='left', padx=(0, 5))
            mass_start = ttk.Entry(stage_frame, width=10)
            mass_start.pack(side='left', padx=(0, 10))
            mass_start.insert(0, "10.0")
            ttk.Label(stage_frame, text=self.get_text("mass_end_short")).pack(side='left', padx=(0, 5))
            mass_end = ttk.Entry(stage_frame, width=10)
            mass_end.pack(side='left', padx=(0, 10))
            mass_end.insert(0, "5.0")
            ttk.Label(stage_frame, text=self.get_text("isp_short")).pack(side='left', padx=(0, 5))
            isp = ttk.Entry(stage_frame, width=10)
            isp.pack(side='left')
            isp.insert(0, "320")
            self.stage_entries.append((mass_start, mass_end, isp))
    
    def update_stages(self, event=None):
        try:
            num = int(self.stages.get())
            if num < 1:
                num = 1
                self.stages.set(1)
            self.create_stage_inputs(num)
        except ValueError:
            pass
    
    def get_gravity_value(self, gravity_str):
        try:
            if '(' in gravity_str:
                return float(gravity_str.split('(')[0].strip())
            return float(gravity_str)
        except:
            return 9.81
    
    def calculate_delta_v(self):
        try:
            num_stages = int(self.stages.get())
            gravity = self.get_gravity_value(self.gravity.get())
            
            if num_stages == 1:
                mass_start = float(self.mass_start.get())
                mass_end = float(self.mass_end.get())
                isp = float(self.isp.get())
                if mass_start <= 0 or mass_end <= 0 or mass_start <= mass_end:
                    messagebox.showerror(self.get_text("error"), self.get_text("mass_error"))
                    return
                if isp <= 0:
                    messagebox.showerror(self.get_text("error"), self.get_text("isp_error"))
                    return
                delta_v = isp * gravity * math.log(mass_start / mass_end)
                self.display_result([(1, mass_start, mass_end, isp, delta_v)], gravity)
            else:
                total_delta_v = 0
                results = []
                for i, (mass_start_entry, mass_end_entry, isp_entry) in enumerate(self.stage_entries):
                    mass_start = float(mass_start_entry.get())
                    mass_end = float(mass_end_entry.get())
                    isp = float(isp_entry.get())
                    if mass_start <= 0 or mass_end <= 0 or mass_start <= mass_end:
                        messagebox.showerror(self.get_text("error"), f"{self.get_text('stage')} {i+1}: {self.get_text('mass_error')}")
                        return
                    if isp <= 0:
                        messagebox.showerror(self.get_text("error"), f"{self.get_text('stage')} {i+1}: {self.get_text('isp_error')}")
                        return
                    delta_v = isp * gravity * math.log(mass_start / mass_end)
                    total_delta_v += delta_v
                    results.append((i+1, mass_start, mass_end, isp, delta_v))
                self.display_result(results, gravity, total_delta_v)
        except ValueError:
            messagebox.showerror(self.get_text("error"), self.get_text("value_error"))
        except Exception as e:
            messagebox.showerror(self.get_text("error"), str(e))
    
    def display_result(self, results, gravity, total_delta_v=None):
        self.result_text.delete('1.0', tk.END)
        body = self.gravity.get().split('(')[-1].replace(')', '') if '(' in self.gravity.get() else ""
        
        if total_delta_v is None:
            stage, m1, m2, isp, dv = results[0]
            text = f"📊 {self.get_text('results_title')}\n"
            text += "="*60 + "\n\n"
            text += f"{self.get_text('body')} {body}\n"
            text += f"{self.get_text('gravity_val')} {gravity:.2f} м/с²\n\n"
            text += f"{self.get_text('stage')} {stage}:\n"
            text += f"  {self.get_text('mass_start_short')} {m1:.2f} т\n"
            text += f"  {self.get_text('mass_end_short')} {m2:.2f} т\n"
            text += f"  {self.get_text('isp_short')} {isp:.0f} с\n"
            text += f"  {self.get_text('mass_ratio')} {m1/m2:.3f}\n"
            text += f"  ΔV: {dv:.1f} м/с\n\n"
            text += self.get_orbit_advice(dv, body)
        else:
            text = f"📊 {self.get_text('results_title')}\n"
            text += "="*60 + "\n\n"
            text += f"{self.get_text('body')} {body}\n"
            text += f"{self.get_text('gravity_val')} {gravity:.2f} м/с²\n\n"
            for stage, m1, m2, isp, dv in results:
                text += f"{self.get_text('stage')} {stage}:\n"
                text += f"  {self.get_text('mass_start_short')} {m1:.2f} т\n"
                text += f"  {self.get_text('mass_end_short')} {m2:.2f} т\n"
                text += f"  {self.get_text('isp_short')} {isp:.0f} с\n"
                text += f"  ΔV: {dv:.1f} м/с\n\n"
            text += "="*60 + "\n"
            text += f"{self.get_text('total_dv')} {total_delta_v:.1f} м/с\n\n"
            text += self.get_orbit_advice(total_delta_v, body)
        
        self.result_text.insert('1.0', text)
    
    def get_orbit_advice(self, dv, body):
        req = {"Kerbin": 3400, "Mun": 580, "Duna": 1500}
        if body in req:
            if dv >= req[body]:
                return f"{self.get_text('enough')} {body}\n{self.get_text('stock')} {dv - req[body]:.0f} м/с"
            else:
                return f"{self.get_text('not_enough')} {body}\n{self.get_text('missing')} {req[body] - dv:.0f} м/с"
        return ""
    
    def init_rocket_advisor(self):
        """Советник по сборке ракеты"""
        advisor_frame = ttk.Frame(self.advisor_frame, padding="10")
        advisor_frame.pack(fill='both', expand=True)
        
        # Заголовок
        title = ttk.Label(advisor_frame, text="🛠️ " + self.get_text("advisor_title"), 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 15))
        
        desc = ttk.Label(advisor_frame, text=self.get_text("advisor_desc"), font=('Arial', 10))
        desc.pack(pady=(0, 20))
        
        # Основной фрейм для параметров
        params_frame = ttk.Frame(advisor_frame)
        params_frame.pack(fill='x', pady=10)
        
        # Цель миссии
        ttk.Label(params_frame, text=self.get_text("mission_target")).grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.mission_target = ttk.Combobox(params_frame, width=25, 
                                          values=[self.get_text("target_orbit"), 
                                                  self.get_text("target_landing"), 
                                                  self.get_text("target_interplanetary")])
        self.mission_target.grid(row=0, column=1, pady=5, padx=5)
        self.mission_target.set(self.get_text("target_orbit"))
        
        # Размер ракеты
        ttk.Label(params_frame, text=self.get_text("rocket_size")).grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.rocket_size = ttk.Combobox(params_frame, width=25,
                                       values=[self.get_text("size_small"), 
                                               self.get_text("size_medium"), 
                                               self.get_text("size_large"), 
                                               self.get_text("size_heavy")])
        self.rocket_size.grid(row=1, column=1, pady=5, padx=5)
        self.rocket_size.set(self.get_text("size_medium"))
        
        # Кнопка
        advise_btn = ttk.Button(advisor_frame, text=self.get_text("get_advice"), 
                               command=self.show_rocket_advice)
        advise_btn.pack(pady=15)
        
        # Результат
        result_frame = ttk.LabelFrame(advisor_frame, text=self.get_text("results"), padding="10")
        result_frame.pack(fill='both', expand=True)
        
        self.advice_text = tk.Text(result_frame, height=12, width=70, font=('Courier', 10),
                                  bg=self.text_bg if hasattr(self, 'text_bg') else '#2a3a5a',
                                  fg=self.text_fg if hasattr(self, 'text_fg') else 'white')
        self.advice_text.pack(fill='both', expand=True)
        self.advice_text.insert('1.0', self.get_text("no_advice"))
    
    def show_rocket_advice(self):
        """Показать совет по сборке ракеты"""
        mission = self.mission_target.get()
        size = self.rocket_size.get()
        
        # Рекомендации
        advice = "="*60 + "\n"
        advice += "🛠️ РЕКОМЕНДАЦИИ ПО СБОРКЕ РАКЕТЫ\n"
        advice += "="*60 + "\n\n"
        
        # Определяем целевую ΔV
        target_dv = 0
        if "орбит" in mission or "Orbit" in mission:
            target_dv = 3400
            advice += "🎯 Цель: Выход на орбиту Kerbin\n"
            advice += f"   Требуемая ΔV: ~{target_dv} м/с\n\n"
        elif "посадк" in mission or "Landing" in mission:
            target_dv = 580
            advice += "🎯 Цель: Посадка на Mun\n"
            advice += f"   Требуемая ΔV: ~{target_dv} м/с\n\n"
        elif "межпланет" in mission or "Interplanetary" in mission:
            target_dv = 4500
            advice += "🎯 Цель: Межпланетный перелёт\n"
            advice += f"   Требуемая ΔV: ~{target_dv} м/с\n\n"
        
        # Рекомендации по ступеням
        if "маленьк" in size or "Small" in size:
            stages = 1
            engines = "Terrier, Spark"
            fuel = "Жидкий кислород + Керосин"
            tips = "- Используйте маленькие двигатели для эффективности\n- Легкие баки для уменьшения массы\n- Обратите внимание на TWR (тяговооружённость)"
        elif "средн" in size or "Medium" in size:
            stages = 2
            engines = "Swivel, Reliant, Terrier"
            fuel = "Жидкий кислород + Керосин"
            tips = "- Первая ступень: тяжёлый двигатель (Swivel/Reliant)\n- Вторая ступень: вакуумный двигатель (Terrier)\n- Используйте разделители ступеней"
        elif "больш" in size or "Large" in size:
            stages = 2
            engines = "Mainsail, Skipper, Poodle"
            fuel = "Жидкий кислород + Керосин"
            tips = "- Первая ступень: мощный двигатель (Mainsail/Skipper)\n- Вторая ступень: вакуумный (Poodle)\n- Добавьте стартовые ускорители для увеличения тяги"
        else:  # Тяжёлая
            stages = 3
            engines = "Mammoth, Rhino, Wolfhound"
            fuel = "Жидкий кислород + Керосин или Жидкий водород"
            tips = "- Первая ступень: сверхтяжёлый двигатель (Mammoth)\n- Вторая ступень: вакуумный двигатель (Rhino)\n- Третья ступень: экономичный (Wolfhound)\n- Используйте асимметричную схему для больших грузов"
        
        advice += f"📊 Рекомендации для {size} ракеты:\n\n"
        advice += f"🔹 {self.get_text('stages_count')} {stages}\n"
        advice += f"🔹 {self.get_text('engine_types')}\n   {engines}\n"
        advice += f"🔹 {self.get_text('fuel_types')}\n   {fuel}\n\n"
        advice += f"💡 {self.get_text('tips')}\n"
        for tip in tips.split('\n'):
            advice += f"   {tip}\n"
        
        advice += "\n" + "="*60 + "\n"
        advice += f"⚠️ Общая рекомендация: Стремитесь к {target_dv} м/с ΔV\n"
        advice += "   Следите за TWR (должен быть >1.0 на старте)\n"
        advice += "   Не забывайте про систему спасения (парашюты)\n"
        
        self.advice_text.delete('1.0', tk.END)
        self.advice_text.insert('1.0', advice)
    
    def init_placeholder_tabs(self):
        """Заглушки для остальных вкладок"""
        # Орбитальная механика
        orbit_inner = ttk.Frame(self.orbit_frame)
        orbit_inner.pack(expand=True)
        orbit_label = ttk.Label(orbit_inner, 
                               text="🛰️ " + self.get_text("orbit_title").upper() + 
                               "\n\n• Расчёт орбитальных параметров\n• Скорость на орбите\n• Период обращения\n• Гомановский переход\n\n" + 
                               self.get_text("soon"),
                               font=('Arial', 14), justify='center')
        orbit_label.pack(expand=True)
        
        # Посадка/Взлёт
        lander_inner = ttk.Frame(self.lander_frame)
        lander_inner.pack(expand=True)
        lander_label = ttk.Label(lander_inner,
                                text="🌙 " + self.get_text("lander_title").upper() + 
                                "\n\n• Расчёт ΔV для посадки\n• Оптимальная траектория\n• Вертикальная скорость\n• Мягкая посадка\n\n" + 
                                self.get_text("soon"),
                                font=('Arial', 14), justify='center')
        lander_label.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = KSPHelper(root)
    root.mainloop()