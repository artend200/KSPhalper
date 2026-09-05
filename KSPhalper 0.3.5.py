import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os

# ============================
# НАСТРОЙКА СТИЛЯ
# ============================
def setup_style(theme="blue"):
    style = ttk.Style()
    style.theme_use('clam')
    
    if theme == "blue":
        bg_main = "#0d1b2a"
        bg_frame = "#1b2d4a"
        bg_entry = "#1e3a5f"
        fg_text = "#ffffff"
        fg_sub = "#a0c4ff"
        accent = "#3a7bd5"
        accent_hover = "#5a9aff"
    else:
        bg_main = "#f0f2f5"
        bg_frame = "#ffffff"
        bg_entry = "#ffffff"
        fg_text = "#1a1a2e"
        fg_sub = "#4a4a6a"
        accent = "#4a7b9d"
        accent_hover = "#6a9bbd"
    
    style.configure("TFrame", background=bg_main)
    style.configure("TLabel", background=bg_main, foreground=fg_text, font=("Segoe UI", 10))
    style.configure("TLabelframe", background=bg_main, foreground=fg_text, relief="flat", borderwidth=2)
    style.configure("TLabelframe.Label", background=bg_main, foreground=fg_text, font=("Segoe UI", 10, "bold"))
    
    style.configure("TButton", background=accent, foreground="white", borderwidth=0, 
                    focusthickness=0, padding=8, font=("Segoe UI", 10, "bold"))
    style.map("TButton", background=[("active", accent_hover), ("pressed", accent_hover)])
    
    style.configure("TEntry", fieldbackground=bg_entry, foreground=fg_text, 
                    borderwidth=1, relief="flat", padding=6)
    style.configure("TCombobox", fieldbackground=bg_entry, foreground=fg_text, padding=6)
    style.configure("TSpinbox", fieldbackground=bg_entry, foreground=fg_text, padding=6)
    
    style.configure("TNotebook", background=bg_main, borderwidth=0)
    style.configure("TNotebook.Tab", background="#2a3a5a", foreground=fg_text, padding=[12, 6], font=("Segoe UI", 10))
    style.map("TNotebook.Tab", background=[("selected", accent)])
    
    style.configure("TRadiobutton", background=bg_main, foreground=fg_text, font=("Segoe UI", 10))
    style.map("TRadiobutton", foreground=[("active", accent)])
    
    style.configure("TText", background=bg_entry, foreground=fg_text, borderwidth=1, relief="flat")
    
    return bg_main, bg_frame, bg_entry, fg_text, fg_sub, accent

# ============================
# ОСНОВНОЕ ПРИЛОЖЕНИЕ
# ============================
class KSPHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("KSP Helper — Помощник пилота")
        self.root.geometry("880x760")
        self.root.minsize(800, 650)
        
        self.version = "0.3.5"
        
        self.settings = {"theme": "blue", "hotkey": "Ctrl+Q"}
        self.load_settings()
        
        # Применяем стиль
        self.bg_main, self.bg_frame, self.bg_entry, self.fg_text, self.fg_sub, self.accent = setup_style(self.settings["theme"])
        self.root.configure(bg=self.bg_main)
        
        # === ВЕРХНЯЯ ПАНЕЛЬ ===
        self.header = tk.Frame(root, bg=self.accent, height=60)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)
        
        self.header_label = tk.Label(self.header, text="🚀 KSP HELPER", font=("Segoe UI", 18, "bold"),
                                      bg=self.accent, fg="white")
        self.header_label.pack(side="left", padx=20, pady=10)
        self.header_version = tk.Label(self.header, text=f"v{self.version}", font=("Segoe UI", 10),
                                        bg=self.accent, fg="#d0e4ff")
        self.header_version.pack(side="left", padx=5)
        
        # === ВКЛАДКИ ===
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(15, 10))
        
        self.delta_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.delta_frame, text="📊 Калькулятор ΔV")
        
        self.advisor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.advisor_frame, text="🛠️ Советник")
        
        self.orbit_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.orbit_frame, text="🛰️ Орбитальная механика")
        
        self.lander_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.lander_frame, text="🌙 Посадка/Взлёт")
        
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Настройки")
        
        # === ИНИЦИАЛИЗАЦИЯ ===
        self.init_delta_calculator()
        self.init_rocket_advisor()
        self.init_placeholder_tabs()
        self.init_settings_tab()
        
        # === ВЕРСИЯ ВНИЗУ ===
        self.version_label = tk.Label(root, text=f"ООО «Цветок» • Версия {self.version}",
                                      font=("Segoe UI", 9), fg=self.fg_sub, bg=self.bg_main)
        self.version_label.place(x=15, y=self.root.winfo_height() - 30)
        self.root.bind('<Configure>', self.update_version_position)
        
        self.apply_hotkey()
    
    def update_version_position(self, event=None):
        self.version_label.place(x=15, y=self.root.winfo_height() - 30)
    
    # ============================
    # ЗАГРУЗКА/СОХРАНЕНИЕ
    # ============================
    def load_settings(self):
        try:
            if os.path.exists("ksp_settings.json"):
                with open("ksp_settings.json", "r", encoding="utf-8") as f:
                    self.settings.update(json.load(f))
        except:
            pass
    
    def save_settings(self):
        try:
            with open("ksp_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    # ============================
    # ПРИМЕНЕНИЕ ТЕМЫ (БЕЗ ПЕРЕЗАПУСКА!)
    # ============================
    def apply_theme(self):
        """Применяет тему ко всем элементам интерфейса без перезапуска"""
        theme = self.settings["theme"]
        self.bg_main, self.bg_frame, self.bg_entry, self.fg_text, self.fg_sub, self.accent = setup_style(theme)
        
        # Обновляем фон главного окна
        self.root.configure(bg=self.bg_main)
        
        # Обновляем шапку
        self.header.configure(bg=self.accent)
        self.header_label.configure(bg=self.accent, fg="white")
        self.header_version.configure(bg=self.accent, fg="#d0e4ff")
        
        # Обновляем текстовые поля
        if hasattr(self, 'result_text'):
            self.result_text.configure(bg=self.bg_entry, fg=self.fg_text)
        if hasattr(self, 'advice_text'):
            self.advice_text.configure(bg=self.bg_entry, fg=self.fg_text)
        
        # Обновляем версию внизу
        self.version_label.configure(fg=self.fg_sub, bg=self.bg_main)
        
        # Обновляем все LabelFrame и Label на всех вкладках
        self.update_all_widgets_theme()
        
        # Обновляем стиль ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.bg_main)
        style.configure("TLabel", background=self.bg_main, foreground=self.fg_text)
        style.configure("TLabelframe", background=self.bg_main, foreground=self.fg_text)
        style.configure("TLabelframe.Label", background=self.bg_main, foreground=self.fg_text)
        style.configure("TButton", background=self.accent, foreground="white")
        style.map("TButton", background=[("active", accent_hover), ("pressed", accent_hover)])
        style.configure("TEntry", fieldbackground=self.bg_entry, foreground=self.fg_text)
        style.configure("TCombobox", fieldbackground=self.bg_entry, foreground=self.fg_text)
        style.configure("TSpinbox", fieldbackground=self.bg_entry, foreground=self.fg_text)
        style.configure("TNotebook", background=self.bg_main)
        style.map("TNotebook.Tab", background=[("selected", self.accent)])
        style.configure("TRadiobutton", background=self.bg_main, foreground=self.fg_text)
        style.configure("TText", background=self.bg_entry, foreground=self.fg_text)
    
    def update_all_widgets_theme(self):
        """Обновляет цвет фона у всех виджетов (для Frame, Label, LabelFrame)"""
        for frame in [self.delta_frame, self.advisor_frame, self.orbit_frame, 
                      self.lander_frame, self.settings_frame]:
            self.update_widgets_recursive(frame)
    
    def update_widgets_recursive(self, widget):
        """Рекурсивно обходит все дочерние виджеты и обновляет их фон"""
        try:
            if isinstance(widget, (tk.Frame, ttk.Frame, ttk.LabelFrame)):
                widget.configure(background=self.bg_main)
            elif isinstance(widget, (tk.Label, ttk.Label)):
                widget.configure(background=self.bg_main, foreground=self.fg_text)
            elif isinstance(widget, ttk.Labelframe):
                widget.configure(background=self.bg_main)
            elif isinstance(widget, tk.Text):
                widget.configure(bg=self.bg_entry, fg=self.fg_text)
        except:
            pass
        
        for child in widget.winfo_children():
            self.update_widgets_recursive(child)
    
    # ============================
    # ВКЛАДКА НАСТРОЕК
    # ============================
    def init_settings_tab(self):
        f = ttk.Frame(self.settings_frame, padding=25)
        f.pack(fill='both', expand=True)
        
        tk.Label(f, text="⚙️ Настройки", font=("Segoe UI", 18, "bold"),
                 bg=self.bg_main, fg=self.fg_text).pack(anchor="w", pady=(0, 25))
        
        # Тема
        lf = ttk.LabelFrame(f, text="Тема", padding=15)
        lf.pack(fill='x', pady=(0, 15))
        
        self.theme_var = tk.StringVar(value=self.settings["theme"])
        for text, val in [("🔵 Синяя", "blue"), ("⚪ Светлая", "light")]:
            rb = ttk.Radiobutton(lf, text=text, variable=self.theme_var, value=val, command=self.change_theme)
            rb.pack(anchor='w', pady=2)
        
        # Горячие клавиши
        hf = ttk.LabelFrame(f, text="⌨️ Горячие клавиши", padding=15)
        hf.pack(fill='x', pady=(0, 15))
        
        ttk.Label(hf, text="Аварийное закрытие:").pack(anchor='w')
        self.hotkey_var = tk.StringVar(value=self.settings.get("hotkey", "Ctrl+Q"))
        self.hotkey_combo = ttk.Combobox(
            hf, textvariable=self.hotkey_var,
            values=["Ctrl+Q", "Ctrl+X", "Ctrl+W", "Alt+F4", "Ctrl+Shift+Q", "Ctrl+Alt+X"],
            width=22
        )
        self.hotkey_combo.pack(anchor='w', pady=5)
        self.hotkey_combo.bind('<<ComboboxSelected>>', self.on_hotkey_change)
        ttk.Label(hf, text="⚠️ Сочетание для немедленного закрытия", font=("Segoe UI", 8, "italic"),
                  foreground=self.fg_sub).pack(anchor='w')
        
        ttk.Button(f, text="✅ Применить", command=self.apply_settings).pack(pady=15)
        ttk.Label(f, text="Настройки сохраняются автоматически", font=("Segoe UI", 9, "italic"),
                  foreground=self.fg_sub).pack()
    
    def change_theme(self):
        """Меняет тему мгновенно без перезапуска"""
        self.settings["theme"] = self.theme_var.get()
        self.save_settings()
        self.apply_theme()
    
    def apply_settings(self):
        self.settings["theme"] = self.theme_var.get()
        self.settings["hotkey"] = self.hotkey_var.get()
        self.save_settings()
        self.apply_theme()
        self.apply_hotkey()
        messagebox.showinfo("Успех", "Настройки применены!")
    
    def on_hotkey_change(self, event=None):
        self.apply_hotkey()
        self.save_settings()
    
    # ============================
    # ГОРЯЧИЕ КЛАВИШИ (БЕЗ ПРЕДУПРЕЖДЕНИЯ!)
    # ============================
    def apply_hotkey(self):
        hotkey = self.hotkey_var.get()
        for k in ["Control-q", "Control-x", "Control-w", "Alt-F4", "Control-Shift-q", "Control-Alt-x"]:
            try:
                self.root.unbind_all(k)
            except:
                pass
        self.root.bind_all(self._to_tk(hotkey), self.emergency_exit)
    
    def _to_tk(self, hotkey):
        mp = {"Ctrl": "Control", "Alt": "Alt", "Shift": "Shift", "Q": "q", "X": "x", "W": "w", "F4": "F4"}
        return '<' + '-'.join(mp.get(p, p.lower()) for p in hotkey.split('+')) + '>'
    
    def emergency_exit(self, event=None):
        """Аварийное закрытие программы БЕЗ ПРЕДУПРЕЖДЕНИЯ"""
        self.root.destroy()  # Мгновенное закрытие
    
    # ============================
    # КАЛЬКУЛЯТОР ΔV
    # ============================
    def init_delta_calculator(self):
        main = ttk.Frame(self.delta_frame, padding=15)
        main.pack(fill='both', expand=True)
        
        # Заголовок
        tk.Label(main, text="📊 Калькулятор ΔV", font=("Segoe UI", 18, "bold"),
                 bg=self.bg_main, fg=self.fg_text).pack(anchor="w", pady=(0, 15))
        
        # Параметры
        pf = ttk.LabelFrame(main, text="Параметры ракеты", padding=15)
        pf.pack(fill='x', pady=(0, 15))
        
        # Сетка
        row = 0
        for label, var, default, col in [
            ("Стартовая масса (т):", "mass_start", "10.0", 0),
            ("Конечная масса (т):", "mass_end", "5.0", 2),
            ("Удельный импульс Isp (с):", "isp", "320", 0),
            ("Гравитация (м/с²):", "gravity", "9.81 (Kerbin)", 2),
            ("Количество ступеней:", "stages", "1", 0),
        ]:
            ttk.Label(pf, text=label).grid(row=row, column=col, sticky='w', pady=6, padx=(0, 10))
            if var == "gravity":
                self.gravity = ttk.Combobox(pf, values=[
                    "9.81 (Kerbin)", "1.63 (Mun)", "3.71 (Duna)", "0.16 (Gilly)",
                    "8.87 (Eve)", "10.44 (Kerbol)", "0.98 (Minmus)", "0.30 (Pol)",
                    "0.05 (Bop)", "0.39 (Ike)", "1.83 (Laythe)", "1.31 (Vall)",
                    "1.79 (Tylo)", "0.24 (Eeloo)", "2.94 (Dres)"
                ], width=22)
                self.gravity.grid(row=row, column=col+1, pady=6, sticky='w')
                self.gravity.set(default)
            elif var == "stages":
                self.stages = ttk.Spinbox(pf, from_=1, to=5, width=10)
                self.stages.grid(row=row, column=col+1, pady=6, sticky='w')
                self.stages.set(default)
                self.stages.bind('<<KeyRelease>>', self.update_stages)
            else:
                ent = ttk.Entry(pf, width=14)
                ent.grid(row=row, column=col+1, pady=6, sticky='w')
                ent.insert(0, default)
                setattr(self, var, ent)
            row += 1 if col == 0 else 0
        
        # Быстрые настройки
        qf = ttk.Frame(pf)
        qf.grid(row=4, column=0, columnspan=4, pady=8, sticky='w')
        ttk.Label(qf, text="⚡ Быстрые настройки:").pack(side='left', padx=(0, 10))
        for name, dv, gv in [("Kerbin", 3400, "9.81 (Kerbin)"), ("Mun", 580, "1.63 (Mun)"), ("Duna", 1500, "3.71 (Duna)")]:
            ttk.Button(qf, text=name, command=lambda t=dv, g=gv: self.quick_setup(t, g), width=8).pack(side='left', padx=3)
        
        # Ступени
        self.stages_frame = ttk.LabelFrame(main, text="Параметры ступеней", padding=15)
        self.stages_frame.pack(fill='x', pady=(0, 15))
        self.stage_entries = []
        self.create_stage_inputs(1)
        
        # Кнопка
        ttk.Button(main, text="🚀 Рассчитать ΔV", command=self.calculate_delta_v).pack(pady=10)
        
        # Результаты
        rf = ttk.LabelFrame(main, text="Результаты", padding=15)
        rf.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(rf, height=10, font=("Courier New", 10),
                                   bg=self.bg_entry, fg=self.fg_text, relief="flat", wrap="none")
        self.result_text.pack(fill='both', expand=True)
        self.result_text.insert('1.0', "Введите параметры и нажмите «Рассчитать ΔV»")
    
    def quick_setup(self, target_dv, gravity_value):
        self.gravity.set(gravity_value)
        isp = float(self.isp.get()) if self.isp.get() else 320
        m_start = 10.0
        m_end = m_start / math.exp(target_dv / (isp * 9.81))
        if m_end > 0:
            self.mass_start.delete(0, tk.END)
            self.mass_start.insert(0, f"{m_start:.2f}")
            self.mass_end.delete(0, tk.END)
            self.mass_end.insert(0, f"{m_end:.2f}")
    
    def create_stage_inputs(self, num):
        for w in self.stages_frame.winfo_children():
            w.destroy()
        self.stage_entries = []
        for i in range(num):
            sf = ttk.Frame(self.stages_frame)
            sf.pack(fill='x', pady=4)
            ttk.Label(sf, text=f"Ступень {i+1}:", font=("Segoe UI", 10, "bold")).pack(side='left', padx=(0, 15))
            for lbl, default in [("Старт. масса:", "10.0"), ("Конеч. масса:", "5.0"), ("Isp:", "320")]:
                ttk.Label(sf, text=lbl).pack(side='left', padx=(0, 4))
                e = ttk.Entry(sf, width=8)
                e.pack(side='left', padx=(0, 10))
                e.insert(0, default)
                self.stage_entries.append(e)
    
    def update_stages(self, event=None):
        try:
            num = max(1, int(self.stages.get()))
            self.stages.set(num)
            self.create_stage_inputs(num)
        except:
            pass
    
    def get_gravity_value(self, s):
        try:
            return float(s.split('(')[0].strip())
        except:
            return 9.81
    
    def calculate_delta_v(self):
        try:
            num = int(self.stages.get())
            g = self.get_gravity_value(self.gravity.get())
            if num == 1:
                m1 = float(self.mass_start.get())
                m2 = float(self.mass_end.get())
                isp = float(self.isp.get())
                if m1 <= 0 or m2 <= 0 or m1 <= m2:
                    raise ValueError("Масса должна быть положительной и стартовая > конечной!")
                if isp <= 0:
                    raise ValueError("Isp должен быть положительным!")
                dv = isp * g * math.log(m1 / m2)
                self.display_result([(1, m1, m2, isp, dv)], g)
            else:
                total = 0
                res = []
                for i in range(num):
                    m1 = float(self.stage_entries[i*3].get())
                    m2 = float(self.stage_entries[i*3+1].get())
                    isp = float(self.stage_entries[i*3+2].get())
                    if m1 <= 0 or m2 <= 0 or m1 <= m2:
                        raise ValueError(f"Ступень {i+1}: масса должна быть положительной и стартовая > конечной!")
                    if isp <= 0:
                        raise ValueError(f"Ступень {i+1}: Isp должен быть положительным!")
                    dv = isp * g * math.log(m1 / m2)
                    total += dv
                    res.append((i+1, m1, m2, isp, dv))
                self.display_result(res, g, total)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def display_result(self, results, g, total=None):
        self.result_text.delete('1.0', tk.END)
        body = self.gravity.get().split('(')[-1].replace(')', '')
        txt = "📊 РЕЗУЛЬТАТЫ РАСЧЕТА\n" + "="*60 + "\n\n"
        txt += f"Небесное тело: {body}\nГравитация: {g:.2f} м/с²\n\n"
        
        if total is None:
            st, m1, m2, isp, dv = results[0]
            txt += f"Ступень {st}:\n"
            txt += f"  Старт. масса: {m1:.2f} т\n  Конеч. масса: {m2:.2f} т\n  Isp: {isp:.0f} с\n"
            txt += f"  Массовое число: {m1/m2:.3f}\n  ΔV: {dv:.1f} м/с\n\n"
            txt += self.get_orbit_advice(dv, body)
        else:
            for st, m1, m2, isp, dv in results:
                txt += f"Ступень {st}:\n  Старт. масса: {m1:.2f} т\n  Конеч. масса: {m2:.2f} т\n"
                txt += f"  Isp: {isp:.0f} с\n  ΔV: {dv:.1f} м/с\n\n"
            txt += "="*60 + f"\nИТОГОВАЯ ΔV: {total:.1f} м/с\n\n"
            txt += self.get_orbit_advice(total, body)
        
        self.result_text.insert('1.0', txt)
    
    def get_orbit_advice(self, dv, body):
        req = {"Kerbin": 3400, "Mun": 580, "Duna": 1500, "Eve": 1200, "Laythe": 2900,
               "Tylo": 2300, "Vall": 860, "Minmus": 180, "Moho": 800, "Ike": 480,
               "Dres": 480, "Pol": 120, "Bop": 120, "Eeloo": 620, "Gilly": 20, "Kerbol": 30000}
        if body in req:
            r = req[body]
            return f"✅ ΔV достаточно для {body}\n   Запас: {dv - r:.0f} м/с" if dv >= r else \
                   f"⚠️ ΔV недостаточно для {body}\n   Не хватает: {r - dv:.0f} м/с"
        return ""
    
    # ============================
    # СОВЕТНИК
    # ============================
    def init_rocket_advisor(self):
        f = ttk.Frame(self.advisor_frame, padding=15)
        f.pack(fill='both', expand=True)
        
        tk.Label(f, text="🛠️ Советник по сборке", font=("Segoe UI", 18, "bold"),
                 bg=self.bg_main, fg=self.fg_text).pack(anchor="w", pady=(0, 5))
        ttk.Label(f, text="Выберите цель и размер ракеты → получите рекомендации").pack(anchor="w", pady=(0, 15))
        
        pf = ttk.Frame(f)
        pf.pack(fill='x', pady=5)
        
        ttk.Label(pf, text="Цель миссии:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.mission_target = ttk.Combobox(pf, values=["Выход на орбиту", "Посадка", "Межпланетный перелёт"], width=25)
        self.mission_target.grid(row=0, column=1, padx=5, pady=5)
        self.mission_target.set("Выход на орбиту")
        
        ttk.Label(pf, text="Размер ракеты:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.rocket_size = ttk.Combobox(pf, values=["Маленькая (до 5т)", "Средняя (5-20т)", "Большая (20-50т)", "Тяжёлая (50т+)"], width=25)
        self.rocket_size.grid(row=1, column=1, padx=5, pady=5)
        self.rocket_size.set("Средняя (5-20т)")
        
        ttk.Button(f, text="💡 Получить совет", command=self.show_rocket_advice).pack(pady=15)
        
        rf = ttk.LabelFrame(f, text="Результат", padding=15)
        rf.pack(fill='both', expand=True)
        self.advice_text = tk.Text(rf, height=12, font=("Courier New", 10),
                                   bg=self.bg_entry, fg=self.fg_text, relief="flat")
        self.advice_text.pack(fill='both', expand=True)
        self.advice_text.insert('1.0', "Выберите параметры и нажмите «Получить совет»")
    
    def show_rocket_advice(self):
        mission = self.mission_target.get()
        size = self.rocket_size.get()
        
        target = {"Выход на орбиту": (3400, "Kerbin"), "Посадка": (580, "Mun"), "Межпланетный перелёт": (4500, "межпланетный")}
        dv, name = target.get(mission, (0, ""))
        
        stages_map = {
            "Маленькая (до 5т)": (1, "Terrier, Spark", "Жидкий кислород + Керосин",
                                  "- Используйте маленькие двигатели\n- Легкие баки\n- Следите за TWR"),
            "Средняя (5-20т)": (2, "Swivel, Reliant, Terrier", "Жидкий кислород + Керосин",
                                "- Первая ступень: тяжёлый двигатель\n- Вторая: вакуумный (Terrier)\n- Используйте разделители"),
            "Большая (20-50т)": (2, "Mainsail, Skipper, Poodle", "Жидкий кислород + Керосин",
                                 "- Первая ступень: мощный двигатель\n- Вторая: вакуумный (Poodle)\n- Добавьте ускорители"),
            "Тяжёлая (50т+)": (3, "Mammoth, Rhino, Wolfhound", "Жидкий кислород + Керосин или Жидкий водород",
                               "- Первая: сверхтяжёлый (Mammoth)\n- Вторая: вакуумный (Rhino)\n- Третья: экономичный (Wolfhound)")
        }
        stages, engines, fuel, tips = stages_map.get(size, (1, "", "", ""))
        
        txt = "="*60 + "\n🛠️ РЕКОМЕНДАЦИИ ПО СБОРКЕ РАКЕТЫ\n" + "="*60 + "\n\n"
        txt += f"🎯 Цель: {mission}\n   Требуемая ΔV: ~{dv} м/с\n\n"
        txt += f"📊 Рекомендации для {size} ракеты:\n\n"
        txt += f"🔹 Ступеней: {stages}\n🔹 Двигатели: {engines}\n🔹 Топливо: {fuel}\n\n"
        txt += "💡 Советы:\n" + "\n".join(f"   {t}" for t in tips.split("\n")) + "\n\n"
        txt += "="*60 + f"\n⚠️ Стремитесь к {dv} м/с ΔV\n   TWR > 1.0 на старте\n   Не забывайте парашюты!"
        
        self.advice_text.delete('1.0', tk.END)
        self.advice_text.insert('1.0', txt)
    
    # ============================
    # ЗАГЛУШКИ
    # ============================
    def init_placeholder_tabs(self):
        for frame, title in [(self.orbit_frame, "ОРБИТАЛЬНАЯ МЕХАНИКА"),
                             (self.lander_frame, "ПОСАДКА И ВЗЛЁТ")]:
            f = ttk.Frame(frame)
            f.pack(expand=True)
            tk.Label(f, text=f"🛰️ {title}" if "ОРБИТ" in title else f"🌙 {title}",
                     font=("Segoe UI", 18, "bold"), bg=self.bg_main, fg=self.fg_text).pack(pady=20)
            tk.Label(f, text="⏳ СКОРО БУДЕТ!", font=("Segoe UI", 14, "italic"),
                     bg=self.bg_main, fg=self.fg_sub).pack()

# ============================
# ЗАПУСК
# ============================
if __name__ == "__main__":
    root = tk.Tk()
    app = KSPHelper(root)
    root.mainloop()