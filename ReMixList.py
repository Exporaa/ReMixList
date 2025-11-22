import os
import time
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime, timedelta
import ctypes
from ctypes import wintypes
import calendar

# --- KAMUS BAHASA (DICTIONARY) ---
TRANSLATIONS = {
    "en": {
        "app_title": "ReMixList v2.0",
        "sub_title": "by Expora (Multi-Language Edition)",
        "frame_1": "1. Select Music Folder",
        "btn_browse": "Browse...",
        "btn_clear": "Clear",
        "frame_2": "2. Date Modified (Primary Time)",
        "btn_set_now": "Set to Now",
        "frame_3": "3. Interval Between Songs",
        "lbl_interval": "Time gap per song:",
        "units": ["Seconds", "Minutes", "Hours", "Days"],
        "frame_4": "4. Date Created Settings (Optional)",
        "chk_create": "Change 'Date Created' too?",
        "rb_sync": "Sync with Date Modified (Simple)",
        "rb_custom": "Set Custom Time (Advanced)",
        "btn_run": "SHUFFLE NOW!",
        "status_ready": "Ready...",
        "status_working": "Working...",
        "status_done": "Done!",
        "msg_folder_err": "Folder not found or empty!",
        "msg_date_err": "Invalid Date format!",
        "msg_confirm_title": "Start Shuffle?",
        "msg_confirm_body": "Target: {}\nStart Time: {}\n\nProceed?",
        "msg_success": "Successfully processed {} songs!",
        "msg_empty": "No audio files found!",
        "lbl_thn": "Yr", "lbl_bln": "Mo", "lbl_tgl": "Day", 
        "lbl_jam": "Hr", "lbl_mnt": "Min", "lbl_dtk": "Sec",
        "menu_lang": "Language", "menu_help": "Help", 
        "help_body": "Go to 'Language' menu at the top to change interface language."
    },
    "id": {
        "app_title": "ReMixList v2.0",
        "sub_title": "oleh Expora (Edisi Multi-Bahasa)",
        "frame_1": "1. Pilih Lokasi Folder Lagu",
        "btn_browse": "Cari...",
        "btn_clear": "Hapus",
        "frame_2": "2. Waktu Modified (Waktu Utama)",
        "btn_set_now": "Set Waktu Sekarang",
        "frame_3": "3. Jarak Antar Lagu (Interval)",
        "lbl_interval": "Jeda setiap lagu:",
        "units": ["Detik", "Menit", "Jam", "Hari"],
        "frame_4": "4. Pengaturan Date Created (Opsional)",
        "chk_create": "Ubah juga 'Date Created'?",
        "rb_sync": "Samakan dengan Date Modified (Simpel)",
        "rb_custom": "Atur Waktu Sendiri (Advanced)",
        "btn_run": "EKSEKUSI SEMUA!",
        "status_ready": "Siap...",
        "status_working": "Sedang bekerja...",
        "status_done": "Selesai!",
        "msg_folder_err": "Folder tidak ditemukan/kosong!",
        "msg_date_err": "Format tanggal salah!",
        "msg_confirm_title": "Mulai Acak?",
        "msg_confirm_body": "Target: {}\nWaktu Mulai: {}\n\nLanjut?",
        "msg_success": "Berhasil memproses {} lagu!",
        "msg_empty": "Tidak ada file lagu ditemukan!",
        "lbl_thn": "Thn", "lbl_bln": "Bln", "lbl_tgl": "Tgl", 
        "lbl_jam": "Jam", "lbl_mnt": "Mnt", "lbl_dtk": "Dtk",
        "menu_lang": "Bahasa", "menu_help": "Bantuan",
        "help_body": "Buka menu 'Bahasa' di bagian atas untuk mengganti bahasa aplikasi."
    },
    "jp": {
        "app_title": "ReMixList v2.0",
        "sub_title": "Expora作 (多言語版)",
        "frame_1": "1. 音楽フォルダを選択",
        "btn_browse": "参照...",
        "btn_clear": "クリア",
        "frame_2": "2. 更新日時 (メイン)",
        "btn_set_now": "現在時刻に設定",
        "frame_3": "3. 曲の間隔 (インターバル)",
        "lbl_interval": "曲ごとの間隔:",
        "units": ["秒", "分", "時間", "日"],
        "frame_4": "4. 作成日時の設定 (オプション)",
        "chk_create": "「作成日時」も変更しますか？",
        "rb_sync": "更新日時と同じにする (簡単)",
        "rb_custom": "自分で時間を設定 (詳細)",
        "btn_run": "シャッフル開始！",
        "status_ready": "準備完了...",
        "status_working": "処理中...",
        "status_done": "完了！",
        "msg_folder_err": "フォルダが見つからないか、空です！",
        "msg_date_err": "日付の形式が無効です！",
        "msg_confirm_title": "開始しますか？",
        "msg_confirm_body": "対象: {}\n開始時間: {}\n\n実行しますか？",
        "msg_success": "{} 曲の処理に成功しました！",
        "msg_empty": "音声ファイルが見つかりません！",
        "lbl_thn": "年", "lbl_bln": "月", "lbl_tgl": "日", 
        "lbl_jam": "時", "lbl_mnt": "分", "lbl_dtk": "秒",
        "menu_lang": "言語 (Language)", "menu_help": "ヘルプ",
        "help_body": "上部の「言語」メニューからインターフェース言語を変更できます。"
    },
    "cn": {
        "app_title": "ReMixList v2.0",
        "sub_title": "Expora 制作 (多语言版)",
        "frame_1": "1. 选择音乐文件夹",
        "btn_browse": "浏览...",
        "btn_clear": "清除",
        "frame_2": "2. 修改时间 (主要)",
        "btn_set_now": "设为当前时间",
        "frame_3": "3. 歌曲间隔",
        "lbl_interval": "每首歌间隔:",
        "units": ["秒", "分", "小时", "天"],
        "frame_4": "4. 创建时间设置 (可选)",
        "chk_create": "同时也修改“创建时间”？",
        "rb_sync": "与修改时间同步 (简单)",
        "rb_custom": "自定义时间 (高级)",
        "btn_run": "立即混洗！",
        "status_ready": "就绪...",
        "status_working": "处理中...",
        "status_done": "完成！",
        "msg_folder_err": "未找到文件夹或文件夹为空！",
        "msg_date_err": "日期格式无效！",
        "msg_confirm_title": "开始混洗？",
        "msg_confirm_body": "目标: {}\n开始时间: {}\n\n继续吗？",
        "msg_success": "成功处理 {} 首歌！",
        "msg_empty": "未找到音频文件！",
        "lbl_thn": "年", "lbl_bln": "月", "lbl_tgl": "日", 
        "lbl_jam": "时", "lbl_mnt": "分", "lbl_dtk": "秒",
        "menu_lang": "语言 (Language)", "menu_help": "帮助",
        "help_body": "请使用顶部的“语言”菜单更改界面语言。"
    },
    "ru": {
        "app_title": "ReMixList v2.0",
        "sub_title": "от Expora (Мультиязычная версия)",
        "frame_1": "1. Выберите папку с музыкой",
        "btn_browse": "Обзор...",
        "btn_clear": "Очистить",
        "frame_2": "2. Дата изменения (Основная)",
        "btn_set_now": "Текущее время",
        "frame_3": "3. Интервал между треками",
        "lbl_interval": "Пауза между треками:",
        "units": ["Сек", "Мин", "Час", "Дни"],
        "frame_4": "4. Дата создания (Опционально)",
        "chk_create": "Изменить также 'Дату создания'?",
        "rb_sync": "Синхронизировать с датой изменения",
        "rb_custom": "Установить своё время (Дополнительно)",
        "btn_run": "ПЕРЕМЕШАТЬ!",
        "status_ready": "Готово...",
        "status_working": "Обработка...",
        "status_done": "Готово!",
        "msg_folder_err": "Папка не найдена или пуста!",
        "msg_date_err": "Неверный формат даты!",
        "msg_confirm_title": "Начать?",
        "msg_confirm_body": "Цель: {}\nВремя начала: {}\n\nПродолжить?",
        "msg_success": "Успешно обработано {} треков!",
        "msg_empty": "Аудиофайлы не найдены!",
        "lbl_thn": "Г", "lbl_bln": "М", "lbl_tgl": "Д", 
        "lbl_jam": "Ч", "lbl_mnt": "Мин", "lbl_dtk": "Сек",
        "menu_lang": "Язык (Language)", "menu_help": "Помощь",
        "help_body": "Используйте меню 'Язык' сверху для смены языка интерфейса."
    }
}

# --- TRIK KHUSUS WINDOWS ---
def set_file_creation_time(path, timestamp):
    try:
        timestamp = int((timestamp * 10000000) + 116444736000000000)
        handle = ctypes.windll.kernel32.CreateFileW(path, 256, 0, None, 3, 128, None)
        if handle == -1: return
        create_time = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
        ctypes.windll.kernel32.SetFileTime(handle, ctypes.byref(create_time), None, None)
        ctypes.windll.kernel32.CloseHandle(handle)
    except: pass

# --- APLIKASI UTAMA ---
class AudioShufflerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x730")
        self.root.resizable(False, True)
        
        # Default Language
        self.lang_code = "en"

        # Style Setup
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 9))

        # --- MENU BAR (FITUR BARU) ---
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        self.setup_menu()

        # --- UI COMPONENTS ---
        # JUDUL
        self.lbl_title = tk.Label(root, font=("Segoe UI", 14, "bold"))
        self.lbl_title.pack(pady=(10, 0))
        self.lbl_subtitle = tk.Label(root, font=("Segoe UI", 9))
        self.lbl_subtitle.pack(pady=(0,10))

        # AREA 1
        self.fr_1 = tk.LabelFrame(root, font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.fr_1.pack(fill="x", padx=15, pady=5)
        self.path_var = tk.StringVar()
        tk.Entry(self.fr_1, textvariable=self.path_var, width=45).grid(row=0, column=0, padx=(0, 5))
        self.btn_browse = tk.Button(self.fr_1, command=self.browse_folder, width=8)
        self.btn_browse.grid(row=0, column=1, padx=2)
        self.btn_clear = tk.Button(self.fr_1, command=self.clear_path, bg="#ffcccc", width=6)
        self.btn_clear.grid(row=0, column=2, padx=2)

        # AREA 2
        self.fr_2 = tk.LabelFrame(root, font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.fr_2.pack(fill="x", padx=15, pady=5)
        self.btn_set_now_mod = tk.Button(self.fr_2, command=lambda: self.set_current_time(self.mod_vars), bg="#f0f0f0", font=("Segoe UI", 8))
        self.btn_set_now_mod.pack(anchor="e", pady=2)
        self.mod_entries, self.mod_vars = self.create_date_inputs(self.fr_2)

        # AREA 3
        self.fr_3 = tk.LabelFrame(root, font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.fr_3.pack(fill="x", padx=15, pady=5)
        self.lbl_interval = tk.Label(self.fr_3)
        self.lbl_interval.pack(side="left")
        self.interval_val = tk.Spinbox(self.fr_3, from_=0, to=999, width=5)
        self.interval_val.delete(0, "end"); self.interval_val.insert(0, "1")
        self.interval_val.pack(side="left", padx=5)
        self.interval_unit = ttk.Combobox(self.fr_3, state="readonly", width=8)
        self.interval_unit.pack(side="left")

        # AREA 4
        self.fr_4 = tk.LabelFrame(root, font=("Segoe UI", 9, "bold"), padx=10, pady=10, fg="blue")
        self.fr_4.pack(fill="x", padx=15, pady=5)
        self.use_created = tk.BooleanVar(value=False)
        self.chk_create = tk.Checkbutton(self.fr_4, variable=self.use_created, command=self.toggle_created_options, font=("Segoe UI", 9, "bold"))
        self.chk_create.pack(anchor="w")
        
        self.created_mode = tk.StringVar(value="sync")
        self.frame_c_opts = tk.Frame(self.fr_4)
        self.frame_c_opts.pack(fill="x", padx=20, pady=5)
        self.rb_sync = tk.Radiobutton(self.frame_c_opts, variable=self.created_mode, value="sync", command=self.toggle_created_inputs)
        self.rb_sync.pack(anchor="w")
        self.rb_custom = tk.Radiobutton(self.frame_c_opts, variable=self.created_mode, value="custom", command=self.toggle_created_inputs)
        self.rb_custom.pack(anchor="w")

        self.frame_c_inputs = tk.Frame(self.frame_c_opts)
        self.frame_c_inputs.pack(pady=5)
        self.btn_set_now_cre = tk.Button(self.frame_c_inputs, command=lambda: self.set_current_time(self.cre_vars), bg="#f0f0f0", font=("Segoe UI", 8))
        self.btn_set_now_cre.pack(anchor="e", pady=2)
        self.cre_entries, self.cre_vars = self.create_date_inputs(self.frame_c_inputs)
        
        self.toggle_created_options()

        # EXECUTE BUTTON
        self.btn_run = tk.Button(root, command=self.run_shuffle, bg="lightgreen", font=("Segoe UI", 12, "bold"), height=2, width=30)
        self.btn_run.pack(pady=20)
        self.status_label = tk.Label(root, fg="blue")
        self.status_label.pack(pady=(0, 10))

        # Set Initial Language
        self.change_language("en")

    # --- SETUP MENU BAR ---
    def setup_menu(self):
        # Menu Language
        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Language", menu=self.lang_menu)
        
        self.lang_var = tk.StringVar(value="en")
        languages = [
            ("English", "en"),
            ("Bahasa Indonesia", "id"),
            ("日本語 (Japanese)", "jp"),
            ("简体中文 (Chinese)", "cn"),
            ("Русский (Russian)", "ru")
        ]
        for text, code in languages:
            self.lang_menu.add_radiobutton(label=text, variable=self.lang_var, value=code, command=self.on_lang_change)

        # Menu Help
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Info", command=self.show_help)

    def on_lang_change(self):
        self.change_language(self.lang_var.get())

    def change_language(self, code):
        self.lang_code = code
        t = TRANSLATIONS[code]

        # Update Titles
        self.root.title(t["app_title"])
        self.lbl_title.config(text=t["app_title"])
        self.lbl_subtitle.config(text=t["sub_title"])

        # Update Frames
        self.fr_1.config(text=t["frame_1"])
        self.fr_2.config(text=t["frame_2"])
        self.fr_3.config(text=t["frame_3"])
        self.fr_4.config(text=t["frame_4"])

        # Update Buttons & Labels
        self.btn_browse.config(text=t["btn_browse"])
        self.btn_clear.config(text=t["btn_clear"])
        self.btn_set_now_mod.config(text=t["btn_set_now"])
        self.btn_set_now_cre.config(text=t["btn_set_now"])
        self.lbl_interval.config(text=t["lbl_interval"])
        self.chk_create.config(text=t["chk_create"])
        self.rb_sync.config(text=t["rb_sync"])
        self.rb_custom.config(text=t["rb_custom"])
        self.btn_run.config(text=t["btn_run"])
        self.status_label.config(text=t["status_ready"])

        # Update Interval Units (Combobox)
        current_idx = self.interval_unit.current()
        self.interval_unit.config(values=t["units"])
        if current_idx == -1: current_idx = 1 # Default Menit
        self.interval_unit.current(current_idx)

        # Update Menu Labels
        self.menu_bar.entryconfig(1, label=t["menu_lang"])
        self.menu_bar.entryconfig(2, label=t["menu_help"])

        # Update Date Labels (Small Inputs)
        # Note: We need to update labels inside create_date_inputs
        keys = ["lbl_thn", "lbl_bln", "lbl_tgl", "lbl_jam", "lbl_mnt", "lbl_dtk"]
        # Helper to recursive update labels inside frames
        self.update_date_labels(self.mod_entries, t, keys)
        self.update_date_labels(self.cre_entries, t, keys)

    def update_date_labels(self, entries_dict, t, keys):
        # entries_dict = {'Thn': SpinboxWidget, ...}
        # But we need to access the Label widget which is the sibling of Spinbox
        # Structure: Frame -> [Label, Spinbox]
        label_map = {
            "Thn": t["lbl_thn"], "Bln": t["lbl_bln"], "Tgl": t["lbl_tgl"],
            "Jam": t["lbl_jam"], "Mnt": t["lbl_mnt"], "Dtk": t["lbl_dtk"]
        }
        for key, widget in entries_dict.items():
            parent = widget.master # The small frame containing Label & Spinbox
            for child in parent.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(text=label_map[key])

    def show_help(self):
        t = TRANSLATIONS[self.lang_code]
        messagebox.showinfo(t["menu_help"], t["help_body"])

    def clear_path(self):
        self.path_var.set("")

    def create_date_inputs(self, parent):
        entries = {}
        variables = {}
        labels = ["Thn", "Bln", "Tgl", "Jam", "Mnt", "Dtk"]
        defaults = [2025, 1, 1, 12, 0, 0]
        limits = {
            "Thn": (1980, 2099), "Bln": (1, 12), "Tgl": (1, 31),
            "Jam": (0, 23), "Mnt": (0, 59), "Dtk": (0, 59)
        }
        
        frame = tk.Frame(parent)
        frame.pack()

        def update_days_limit(*args):
            try:
                y = variables["Thn"].get()
                m = variables["Bln"].get()
                if m < 1: m = 1
                if m > 12: m = 12
                _, max_days = calendar.monthrange(y, m)
                entries["Tgl"].config(to=max_days)
                if variables["Tgl"].get() > max_days:
                    variables["Tgl"].set(max_days)
            except: pass

        for i, (lbl, default) in enumerate(zip(labels, defaults)):
            f = tk.Frame(frame)
            f.grid(row=0, column=i, padx=2)
            tk.Label(f, text=lbl, font=("Arial", 7)).pack() # Text will be updated by change_language
            
            min_val, max_val = limits[lbl]
            var = tk.IntVar(value=default)
            variables[lbl] = var
            
            e = tk.Spinbox(f, from_=min_val, to=max_val, width=4, wrap=True, textvariable=var) 
            e.pack()
            entries[lbl] = e
            
            if lbl in ["Thn", "Bln"]:
                var.trace_add("write", update_days_limit)

        update_days_limit()
        return entries, variables

    def set_current_time(self, var_dict):
        now = datetime.now()
        vals = [now.year, now.month, now.day, now.hour, now.minute, now.second]
        keys = ["Thn", "Bln", "Tgl", "Jam", "Mnt", "Dtk"]
        for k, v in zip(keys, vals):
            var_dict[k].set(v)

    def toggle_created_options(self):
        if self.use_created.get():
            self.rb_sync.config(state="normal")
            self.rb_custom.config(state="normal")
            self.toggle_created_inputs()
        else:
            self.rb_sync.config(state="disabled")
            self.rb_custom.config(state="disabled")
            for w in self.frame_c_inputs.winfo_children():
                for child in w.winfo_children():
                    try: child.config(state="disabled")
                    except: pass

    def toggle_created_inputs(self):
        state = "normal" if (self.use_created.get() and self.created_mode.get() == "custom") else "disabled"
        for w in self.frame_c_inputs.winfo_children():
             if isinstance(w, tk.Button): w.config(state=state)
             else:
                 for child in w.winfo_children():
                     for sub in child.winfo_children(): sub.config(state=state)

    def get_date_from_vars(self, var_dict):
        try:
            return datetime(
                var_dict["Thn"].get(), var_dict["Bln"].get(), var_dict["Tgl"].get(),
                var_dict["Jam"].get(), var_dict["Mnt"].get(), var_dict["Dtk"].get()
            )
        except ValueError: return None

    def browse_folder(self):
        f = filedialog.askdirectory()
        if f: self.path_var.set(f)

    def run_shuffle(self):
        t = TRANSLATIONS[self.lang_code] # Get current language dict
        
        folder = self.path_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", t["msg_folder_err"])
            return

        start_mod = self.get_date_from_vars(self.mod_vars)
        start_cre = self.get_date_from_vars(self.cre_vars)
        
        if not start_mod:
            messagebox.showerror("Error", t["msg_date_err"])
            return
        
        if self.use_created.get() and self.created_mode.get() == "custom" and not start_cre:
             messagebox.showerror("Error", t["msg_date_err"])
             return

        msg = t["msg_confirm_body"].format(folder, start_mod)
        if not messagebox.askyesno(t["msg_confirm_title"], msg): return

        try:
            exts = ('.flac', '.mp3', '.wav', '.aiff', '.m4a', '.ogg', '.wma', '.opus', '.dsd', '.dsf')
            files = []
            for r, d, f in os.walk(folder):
                for file in f:
                    if file.lower().endswith(exts):
                        files.append(os.path.join(r, file))
            
            if not files: 
                messagebox.showwarning("Empty", t["msg_empty"])
                return

            random.shuffle(files)
            
            val = int(self.interval_val.get())
            # Use index because text changes per language
            unit_idx = self.interval_unit.current() 
            
            delta = timedelta(seconds=0)
            if unit_idx == 0: delta = timedelta(seconds=val)    # Seconds
            elif unit_idx == 1: delta = timedelta(minutes=val)  # Minutes
            elif unit_idx == 2: delta = timedelta(hours=val)    # Hours
            elif unit_idx == 3: delta = timedelta(days=val)     # Days

            curr_mod = start_mod
            curr_cre = start_cre if start_cre else start_mod

            count = 0
            self.status_label.config(text=t["status_working"])
            self.root.update()

            for fpath in files:
                ts_mod = curr_mod.timestamp()
                os.utime(fpath, (ts_mod, ts_mod))

                if self.use_created.get():
                    target_cre = curr_mod if self.created_mode.get() == "sync" else curr_cre
                    set_file_creation_time(fpath, target_cre.timestamp())
                    if self.created_mode.get() == "custom": curr_cre += delta

                curr_mod += delta
                count += 1

            self.status_label.config(text=t["status_done"])
            messagebox.showinfo("Success", t["msg_success"].format(count))

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioShufflerApp(root)
    root.mainloop()