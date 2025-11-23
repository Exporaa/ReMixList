import os
import time
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime, timedelta
import ctypes
from ctypes import wintypes
import calendar
import re

# --- SETUP LIBRARY DRAG & DROP ---
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    messagebox.showerror("Error", "Library 'tkinterdnd2' belum diinstall!\nKetik di CMD: pip install tkinterdnd2")
    raise SystemExit

# --- KAMUS BAHASA (DICTIONARY) v3.1 ---
TRANSLATIONS = {
    "en": {
        "app_title": "ReMixList v3.1",
        "sub_title": "by Expora",
        "tab_file": "🎵 Shuffle Files",
        "tab_folder": "📂 Sort Folders",
        "frame_1": "1. Select Music Folder",
        "btn_browse": "Browse...",
        "btn_clear": "Clear",
        "frame_2": "2. Start Time",
        "btn_set_now": "Set to Now",
        "frame_3": "3. Interval",
        "lbl_interval": "Gap per item:",
        "units": ["Seconds", "Minutes", "Hours", "Days"],
        "frame_4": "4. Date Created (Optional)",
        "chk_create": "Change 'Date Created' too?",
        "rb_sync": "Sync with Modified",
        "rb_custom": "Custom Time",
        "btn_run_file": "SHUFFLE FILES!",
        
        # Tab 2
        "lbl_folder_list": "1. Folder List:",
        "lbl_tip": "💡 Tip: Drag folders here to add them.",
        "btn_add_folder": "Add Folder",
        "btn_remove": "Remove",
        "btn_up": "Up",
        "btn_down": "Down",
        "btn_clear_list": "Clear",
        "frame_int_folder": "3a. Interval Between FOLDERS",
        "lbl_int_folder": "Base Gap per Folder:",
        "frame_int_file": "3b. Interval Between FILES (Inside)",
        "lbl_int_file": "Gap per File:",
        "frame_4_folder": "4. Folder 'Date Created' (Optional)",
        "frame_opts": "5. Content Options",
        "chk_sync_content": "Process files inside?",
        "lbl_sync_hint": "(Files will match the Folder's new timestamps)",
        "btn_run_folder": "PROCESS FOLDERS!",
        "status_ready": "Ready...",
        "status_working": "Working...",
        "status_done": "Done!",
        "msg_success": "Success! Processed {} items.",
        "msg_folder_err": "Select at least one folder!",
        "msg_date_err": "Invalid Date!",
        "msg_smart_title": "Smart Import",
        "msg_smart_body": "Found {} sub-folders in '{}'. Add them individually?",
        "lbl_thn": "Yr", "lbl_bln": "Mo", "lbl_tgl": "Day", "lbl_jam": "Hr", "lbl_mnt": "Min", "lbl_dtk": "Sec",
        "menu_lang": "Language", "menu_help": "Help", 
        "help_body": "v3.1 Update: Folder 'Created Date' now correctly follows the Smart Interval logic (skips time if folder content is large)."
    },
    "id": {
        "app_title": "ReMixList v3.1",
        "sub_title": "oleh Expora",
        "tab_file": "🎵 Acak File",
        "tab_folder": "📂 Urutkan Folder",
        "frame_1": "1. Pilih Folder Lagu",
        "btn_browse": "Cari...",
        "btn_clear": "Hapus",
        "frame_2": "2. Waktu Mulai",
        "btn_set_now": "Waktu Sekarang",
        "frame_3": "3. Jarak Waktu (Interval)",
        "lbl_interval": "Jeda per item:",
        "units": ["Detik", "Menit", "Jam", "Hari"],
        "frame_4": "4. Date Created (Opsional)",
        "chk_create": "Ubah juga 'Date Created'?",
        "rb_sync": "Samakan dengan Modified",
        "rb_custom": "Atur Sendiri",
        "btn_run_file": "ACAK FILE SEKARANG!",
        "lbl_folder_list": "Daftar Folder:",
        "lbl_tip": "💡 Tips: Drag & Drop folder ke sini.",
        "btn_add_folder": "Tambah Folder (Pintar)",
        "btn_remove": "Hapus",
        "btn_up": "Naik",
        "btn_down": "Turun",
        "btn_clear_list": "Reset",
        "frame_int_folder": "3a. Interval Antar FOLDER",
        "lbl_int_folder": "Jeda Dasar Folder:",
        "frame_int_file": "3b. Interval Antar FILE (Isi Folder)",
        "lbl_int_file": "Jeda Lagu 1 ke 2:",
        "frame_4_folder": "4. 'Date Created' Folder (Opsional)",
        "frame_opts": "5. Opsi Isi Folder",
        "chk_sync_content": "Proses file di dalamnya?",
        "lbl_sync_hint": "(File akan mengikuti waktu baru Folder)",
        "btn_run_folder": "PROSES FOLDER!",
        "status_ready": "Siap...",
        "status_working": "Sedang bekerja...",
        "status_done": "Selesai!",
        "msg_success": "Berhasil! Memproses {} item.",
        "msg_folder_err": "Pilih minimal satu folder!",
        "msg_date_err": "Format tanggal salah!",
        "msg_smart_title": "Import Pintar",
        "msg_smart_body": "Ditemukan {} sub-folder di '{}'. Masukkan satu per satu?",
        "lbl_thn": "Thn", "lbl_bln": "Bln", "lbl_tgl": "Tgl", "lbl_jam": "Jam", "lbl_mnt": "Mnt", "lbl_dtk": "Dtk",
        "menu_lang": "Bahasa", "menu_help": "Bantuan",
        "help_body": "Update v3.1: 'Date Created' Folder sekarang ikut pintar (otomatis loncat waktu jika isi folder penuh)."
    },
    # Fallbacks
    "jp": {"app_title": "ReMixList v3.1", "sub_title": "Expora作", "tab_file": "🎵 ファイル", "tab_folder": "📂 フォルダ", "units": ["秒", "分", "時間", "日"], "lbl_thn": "年", "lbl_bln": "月", "lbl_tgl": "日", "lbl_jam": "時", "lbl_mnt": "分", "lbl_dtk": "秒"},
    "cn": {"app_title": "ReMixList v3.1", "sub_title": "Expora 制作", "tab_file": "🎵 文件", "tab_folder": "📂 文件夹", "units": ["秒", "分", "小时", "天"], "lbl_thn": "年", "lbl_bln": "月", "lbl_tgl": "日", "lbl_jam": "时", "lbl_mnt": "分", "lbl_dtk": "秒"},
    "ru": {"app_title": "ReMixList v3.1", "sub_title": "от Expora", "tab_file": "🎵 Файлы", "tab_folder": "📂 Папки", "units": ["Сек", "Мин", "Час", "Дни"], "lbl_thn": "Г", "lbl_bln": "М", "lbl_tgl": "Д", "lbl_jam": "Ч", "lbl_mnt": "Мин", "lbl_dtk": "Сек"}
}
for lang in ["jp", "cn", "ru"]:
    for key, val in TRANSLATIONS["en"].items():
        if key not in TRANSLATIONS[lang]: TRANSLATIONS[lang][key] = val

# --- KERNEL ACCESS (FIXED) ---
def set_file_creation_time(path, timestamp):
    try:
        timestamp = int((timestamp * 10000000) + 116444736000000000)
        flags_and_attributes = 128 | 33554432 # FILE_ATTRIBUTE_NORMAL | FILE_FLAG_BACKUP_SEMANTICS
        handle = ctypes.windll.kernel32.CreateFileW(path, 256, 0, None, 3, flags_and_attributes, None)
        if handle == -1: return
        create_time = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
        ctypes.windll.kernel32.SetFileTime(handle, ctypes.byref(create_time), None, None)
        ctypes.windll.kernel32.CloseHandle(handle)
    except: pass

class AudioShufflerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x900")
        self.root.resizable(False, True)
        self.lang_code = "en"
        self.folder_data = [] 

        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        self.setup_menu()

        self.lbl_title = tk.Label(root, font=("Segoe UI", 14, "bold"))
        self.lbl_title.pack(pady=(10, 0))
        self.lbl_subtitle = tk.Label(root, font=("Segoe UI", 9))
        self.lbl_subtitle.pack(pady=(0, 5))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Shuffle Files")
        self.setup_tab_shuffle()

        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Sort Folders")
        self.setup_tab_folder()

        self.status_label = tk.Label(root, fg="blue", font=("Segoe UI", 9))
        self.status_label.pack(pady=5)
        self.change_language("en")

    # --- SETUP TAB 1 ---
    def setup_tab_shuffle(self):
        self.fr1_path = tk.LabelFrame(self.tab1, font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.fr1_path.pack(fill="x", padx=10, pady=5)
        self.t1_path_var = tk.StringVar()
        tk.Entry(self.fr1_path, textvariable=self.t1_path_var, width=50).grid(row=0, column=0, padx=5)
        self.t1_btn_browse = tk.Button(self.fr1_path, command=self.t1_browse, width=8)
        self.t1_btn_browse.grid(row=0, column=1, padx=2)
        self.t1_btn_clear = tk.Button(self.fr1_path, command=lambda: self.t1_path_var.set(""), bg="#ffcccc", width=6)
        self.t1_btn_clear.grid(row=0, column=2, padx=2)

        self.fr1_date = tk.LabelFrame(self.tab1, font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.fr1_date.pack(fill="x", padx=10, pady=5)
        self.t1_btn_now = tk.Button(self.fr1_date, command=lambda: self.set_current_time(self.t1_mod_vars), bg="#f0f0f0", font=("Segoe UI", 8))
        self.t1_btn_now.pack(anchor="e", pady=2)
        self.t1_mod_entries, self.t1_mod_vars = self.create_date_inputs(self.fr1_date)

        self.fr1_int = tk.LabelFrame(self.tab1, font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.fr1_int.pack(fill="x", padx=10, pady=5)
        self.t1_lbl_int = tk.Label(self.fr1_int)
        self.t1_lbl_int.pack(side="left")
        self.t1_int_val = tk.Spinbox(self.fr1_int, from_=1, to=59, width=5, wrap=True)
        self.t1_int_val.delete(0, "end"); self.t1_int_val.insert(0, "1")
        self.t1_int_val.pack(side="left", padx=5)
        self.t1_int_unit = ttk.Combobox(self.fr1_int, state="readonly", width=8)
        self.t1_int_unit.pack(side="left")
        self.t1_int_unit.bind("<<ComboboxSelected>>", lambda e: self.update_interval_limit(self.t1_int_unit, self.t1_int_val))

        self.fr1_cre = tk.LabelFrame(self.tab1, font=("Segoe UI", 9, "bold"), padx=10, pady=10, fg="blue")
        self.fr1_cre.pack(fill="x", padx=10, pady=5)
        self.t1_use_cre = tk.BooleanVar(value=False)
        self.t1_chk_cre = tk.Checkbutton(self.fr1_cre, variable=self.t1_use_cre, command=self.t1_toggle_cre, font=("Segoe UI", 9, "bold"))
        self.t1_chk_cre.pack(anchor="w")
        self.t1_cre_mode = tk.StringVar(value="sync")
        self.t1_fr_cre_opts = tk.Frame(self.fr1_cre)
        self.t1_fr_cre_opts.pack(fill="x", padx=20, pady=5)
        self.t1_rb_sync = tk.Radiobutton(self.t1_fr_cre_opts, variable=self.t1_cre_mode, value="sync", command=self.t1_toggle_inputs)
        self.t1_rb_sync.pack(anchor="w")
        self.t1_rb_custom = tk.Radiobutton(self.t1_fr_cre_opts, variable=self.t1_cre_mode, value="custom", command=self.t1_toggle_inputs)
        self.t1_rb_custom.pack(anchor="w")
        self.t1_fr_cre_inp = tk.Frame(self.t1_fr_cre_opts)
        self.t1_fr_cre_inp.pack(pady=5)
        self.t1_btn_cre_now = tk.Button(self.t1_fr_cre_inp, command=lambda: self.set_current_time(self.t1_cre_vars), bg="#f0f0f0", font=("Segoe UI", 8))
        self.t1_btn_cre_now.pack(anchor="e", pady=2)
        self.t1_cre_entries, self.t1_cre_vars = self.create_date_inputs(self.t1_fr_cre_inp)
        self.t1_toggle_cre()

        self.t1_btn_run = tk.Button(self.tab1, command=self.run_shuffle_files, bg="lightgreen", font=("Segoe UI", 11, "bold"), height=2)
        self.t1_btn_run.pack(pady=15, fill="x", padx=50)

    # --- SETUP TAB 2 ---
    def setup_tab_folder(self):
        frame_list = tk.Frame(self.tab2)
        frame_list.pack(fill="both", expand=True, padx=10, pady=5)
        self.t2_lbl_list = tk.Label(frame_list, font=("Segoe UI", 9, "bold"))
        self.t2_lbl_list.pack(anchor="w")
        self.t2_lbl_tip = tk.Label(frame_list, font=("Segoe UI", 8, "italic"), fg="#555")
        self.t2_lbl_tip.pack(anchor="w", pady=(0,5))
        list_cont = tk.Frame(frame_list)
        list_cont.pack(fill="both", expand=True)
        self.folder_listbox = tk.Listbox(list_cont, height=5, selectmode=tk.EXTENDED, activestyle='dotbox')
        self.folder_listbox.pack(side="left", fill="both", expand=True)
        self.folder_listbox.drop_target_register(DND_FILES)
        self.folder_listbox.dnd_bind('<<Drop>>', self.drop_data)
        scrolly = tk.Scrollbar(list_cont, command=self.folder_listbox.yview)
        scrolly.pack(side="right", fill="y")
        self.folder_listbox.config(yscrollcommand=scrolly.set)
        btn_fr = tk.Frame(frame_list)
        btn_fr.pack(fill="x", pady=5)
        self.t2_btn_add = tk.Button(btn_fr, command=self.t2_add_folder, width=18, bg="#e6f3ff")
        self.t2_btn_add.pack(side="left", padx=2)
        self.t2_btn_del = tk.Button(btn_fr, command=self.t2_del_folder, width=8, bg="#ffcccc")
        self.t2_btn_del.pack(side="left", padx=2)
        self.t2_btn_clr = tk.Button(btn_fr, command=self.t2_clear_all, width=8)
        self.t2_btn_clr.pack(side="right", padx=2)
        self.t2_btn_down = tk.Button(btn_fr, text="▼", command=lambda: self.move_item(1), width=4)
        self.t2_btn_down.pack(side="right", padx=2)
        self.t2_btn_up = tk.Button(btn_fr, text="▲", command=lambda: self.move_item(-1), width=4)
        self.t2_btn_up.pack(side="right", padx=2)

        self.fr2_date = tk.LabelFrame(self.tab2, font=("Segoe UI", 9, "bold"), padx=10, pady=5)
        self.fr2_date.pack(fill="x", padx=10, pady=5)
        self.t2_btn_now = tk.Button(self.fr2_date, command=lambda: self.set_current_time(self.t2_mod_vars), bg="#f0f0f0", font=("Segoe UI", 8))
        self.t2_btn_now.pack(anchor="e")
        self.t2_mod_entries, self.t2_mod_vars = self.create_date_inputs(self.fr2_date)

        self.fr2_int_folder = tk.LabelFrame(self.tab2, font=("Segoe UI", 9, "bold"), padx=10, pady=5)
        self.fr2_int_folder.pack(fill="x", padx=10, pady=2)
        self.t2_lbl_int_folder = tk.Label(self.fr2_int_folder)
        self.t2_lbl_int_folder.pack(side="left")
        self.t2_int_val_f = tk.Spinbox(self.fr2_int_folder, from_=1, to=59, width=5, wrap=True)
        self.t2_int_val_f.delete(0, "end"); self.t2_int_val_f.insert(0, "1")
        self.t2_int_val_f.pack(side="left", padx=5)
        self.t2_int_unit_f = ttk.Combobox(self.fr2_int_folder, state="readonly", width=8)
        self.t2_int_unit_f.pack(side="left")
        self.t2_int_unit_f.bind("<<ComboboxSelected>>", lambda e: self.update_interval_limit(self.t2_int_unit_f, self.t2_int_val_f))

        self.fr2_int_file = tk.LabelFrame(self.tab2, font=("Segoe UI", 9, "bold"), padx=10, pady=5)
        self.fr2_int_file.pack(fill="x", padx=10, pady=2)
        self.t2_lbl_int_file = tk.Label(self.fr2_int_file)
        self.t2_lbl_int_file.pack(side="left")
        self.t2_int_val_i = tk.Spinbox(self.fr2_int_file, from_=1, to=59, width=5, wrap=True)
        self.t2_int_val_i.delete(0, "end"); self.t2_int_val_i.insert(0, "1")
        self.t2_int_val_i.pack(side="left", padx=5)
        self.t2_int_unit_i = ttk.Combobox(self.fr2_int_file, state="readonly", width=8)
        self.t2_int_unit_i.pack(side="left")
        self.t2_int_unit_i.bind("<<ComboboxSelected>>", lambda e: self.update_interval_limit(self.t2_int_unit_i, self.t2_int_val_i))

        self.fr2_cre = tk.LabelFrame(self.tab2, font=("Segoe UI", 9, "bold"), padx=10, pady=5, fg="blue")
        self.fr2_cre.pack(fill="x", padx=10, pady=5)
        self.t2_use_cre = tk.BooleanVar(value=False)
        self.t2_chk_cre = tk.Checkbutton(self.fr2_cre, variable=self.t2_use_cre, command=self.t2_toggle_cre, font=("Segoe UI", 9, "bold"))
        self.t2_chk_cre.pack(anchor="w")
        self.t2_cre_mode = tk.StringVar(value="sync")
        self.t2_fr_cre_opts = tk.Frame(self.fr2_cre)
        self.t2_fr_cre_opts.pack(fill="x", padx=20, pady=2)
        self.t2_rb_sync = tk.Radiobutton(self.t2_fr_cre_opts, variable=self.t2_cre_mode, value="sync", command=self.t2_toggle_inputs)
        self.t2_rb_sync.pack(anchor="w")
        self.t2_rb_custom = tk.Radiobutton(self.t2_fr_cre_opts, variable=self.t2_cre_mode, value="custom", command=self.t2_toggle_inputs)
        self.t2_rb_custom.pack(anchor="w")
        self.t2_fr_cre_inp = tk.Frame(self.t2_fr_cre_opts)
        self.t2_fr_cre_inp.pack(pady=2)
        self.t2_btn_cre_now = tk.Button(self.t2_fr_cre_inp, command=lambda: self.set_current_time(self.t2_cre_vars), bg="#f0f0f0", font=("Segoe UI", 8))
        self.t2_btn_cre_now.pack(anchor="e", pady=2)
        self.t2_cre_entries, self.t2_cre_vars = self.create_date_inputs(self.t2_fr_cre_inp)
        self.t2_toggle_cre()

        self.fr2_opts = tk.LabelFrame(self.tab2, font=("Segoe UI", 9, "bold"), padx=10, pady=5, fg="green")
        self.fr2_opts.pack(fill="x", padx=10, pady=5)
        self.t2_sync_var = tk.BooleanVar(value=True)
        self.t2_chk_sync = tk.Checkbutton(self.fr2_opts, variable=self.t2_sync_var, font=("Segoe UI", 9, "bold"))
        self.t2_chk_sync.pack(anchor="w")
        self.t2_lbl_sync_hint = tk.Label(self.fr2_opts, font=("Segoe UI", 8, "italic"), fg="gray")
        self.t2_lbl_sync_hint.pack(anchor="w", padx=20)

        self.t2_btn_run = tk.Button(self.tab2, command=self.run_sort_folders, bg="lightblue", font=("Segoe UI", 11, "bold"), height=2)
        self.t2_btn_run.pack(pady=10, fill="x", padx=50)

    # --- LOGIC UTILS ---
    def drop_data(self, event):
        raw_data = event.data
        paths = re.findall(r'\{.*?\}|\S+', raw_data)
        for p in paths:
            clean_path = p.strip("{}")
            if os.path.isdir(clean_path):
                if clean_path not in self.folder_data:
                    self.folder_data.append(clean_path)
        self.refresh_listbox()

    def t2_add_folder(self):
        parent_folder = filedialog.askdirectory() 
        if parent_folder:
            try:
                subfolders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, d))]
                if subfolders:
                    t = TRANSLATIONS[self.lang_code]
                    msg = t["msg_smart_body"].format(len(subfolders), os.path.basename(parent_folder))
                    choice = messagebox.askyesno(t["msg_smart_title"], msg)
                    if choice:
                        for sub in subfolders:
                            if sub not in self.folder_data: self.folder_data.append(sub)
                    else:
                        if parent_folder not in self.folder_data: self.folder_data.append(parent_folder)
                else:
                    if parent_folder not in self.folder_data: self.folder_data.append(parent_folder)
                self.refresh_listbox()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def t2_del_folder(self):
        sels = self.folder_listbox.curselection()
        if not sels: return
        for i in reversed(sels):
            del self.folder_data[i]
        self.refresh_listbox()

    def t2_clear_all(self):
        self.folder_data.clear()
        self.refresh_listbox()

    def move_item(self, direction):
        sels = self.folder_listbox.curselection()
        if not sels: return
        i = sels[0]
        if direction == -1 and i > 0:
            self.folder_data[i], self.folder_data[i-1] = self.folder_data[i-1], self.folder_data[i]
            self.refresh_listbox()
            self.folder_listbox.selection_set(i-1)
        elif direction == 1 and i < len(self.folder_data) - 1:
            self.folder_data[i], self.folder_data[i+1] = self.folder_data[i+1], self.folder_data[i]
            self.refresh_listbox()
            self.folder_listbox.selection_set(i+1)

    def refresh_listbox(self):
        self.folder_listbox.delete(0, "end")
        for i, folder in enumerate(self.folder_data):
            display_text = f"[{i+1}] {folder}"
            self.folder_listbox.insert("end", display_text)

    # --- SHARED LOGIC ---
    def setup_menu(self):
        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Language", menu=self.lang_menu)
        self.lang_var = tk.StringVar(value="en")
        for txt, code in [("English", "en"), ("Bahasa Indonesia", "id"), ("Japanese", "jp"), ("Chinese", "cn"), ("Russian", "ru")]:
            self.lang_menu.add_radiobutton(label=txt, variable=self.lang_var, value=code, command=self.on_lang_change)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Info", command=lambda: messagebox.showinfo("Info", TRANSLATIONS[self.lang_code]["help_body"]))

    def on_lang_change(self):
        self.change_language(self.lang_var.get())

    def change_language(self, code):
        self.lang_code = code
        t = TRANSLATIONS[code]
        self.root.title(t["app_title"])
        self.lbl_title.config(text=t["app_title"])
        self.lbl_subtitle.config(text=t["sub_title"])
        self.notebook.tab(0, text=t["tab_file"])
        self.notebook.tab(1, text=t["tab_folder"])

        self.fr1_path.config(text=t["frame_1"])
        self.fr1_date.config(text=t["frame_2"])
        self.fr1_int.config(text=t["frame_3"])
        self.fr1_cre.config(text=t["frame_4"])
        self.t1_btn_browse.config(text=t["btn_browse"])
        self.t1_btn_clear.config(text=t["btn_clear"])
        self.t1_btn_now.config(text=t["btn_set_now"])
        self.t1_btn_cre_now.config(text=t["btn_set_now"])
        self.t1_lbl_int.config(text=t["lbl_interval"])
        self.t1_chk_cre.config(text=t["chk_create"])
        self.t1_rb_sync.config(text=t["rb_sync"])
        self.t1_rb_custom.config(text=t["rb_custom"])
        self.t1_btn_run.config(text=t["btn_run_file"])

        self.t2_lbl_list.config(text=t["lbl_folder_list"])
        self.t2_lbl_tip.config(text=t["lbl_tip"])
        self.t2_btn_add.config(text=t["btn_add_folder"])
        self.t2_btn_del.config(text=t["btn_remove"])
        self.t2_btn_clr.config(text=t["btn_clear_list"])
        self.t2_btn_up.config(text=t["btn_up"])
        self.t2_btn_down.config(text=t["btn_down"])
        self.fr2_date.config(text=t["frame_2"])
        self.t2_btn_now.config(text=t["btn_set_now"])
        self.fr2_int_folder.config(text=t["frame_int_folder"])
        self.t2_lbl_int_folder.config(text=t["lbl_int_folder"])
        self.fr2_int_file.config(text=t["frame_int_file"])
        self.t2_lbl_int_file.config(text=t["lbl_int_file"])
        
        # Tab 2 Created
        self.fr2_cre.config(text=t["frame_4_folder"])
        self.t2_chk_cre.config(text=t["chk_create"])
        self.t2_rb_sync.config(text=t["rb_sync"])
        self.t2_rb_custom.config(text=t["rb_custom"])
        self.t2_btn_cre_now.config(text=t["btn_set_now"])

        self.fr2_opts.config(text=t["frame_opts"])
        self.t2_chk_sync.config(text=t["chk_sync_content"])
        self.t2_lbl_sync_hint.config(text=t["lbl_sync_hint"])
        
        self.t2_btn_run.config(text=t["btn_run_folder"])

        self.status_label.config(text=t["status_ready"])
        self.update_combobox(self.t1_int_unit, t["units"])
        self.update_combobox(self.t2_int_unit_f, t["units"])
        self.update_combobox(self.t2_int_unit_i, t["units"])
        
        keys = ["lbl_thn", "lbl_bln", "lbl_tgl", "lbl_jam", "lbl_mnt", "lbl_dtk"]
        self.update_date_labels(self.t1_mod_entries, t, keys)
        self.update_date_labels(self.t1_cre_entries, t, keys)
        self.update_date_labels(self.t2_mod_entries, t, keys)
        self.update_date_labels(self.t2_cre_entries, t, keys)
        
        self.update_interval_limit(self.t1_int_unit, self.t1_int_val)
        self.update_interval_limit(self.t2_int_unit_f, self.t2_int_val_f)
        self.update_interval_limit(self.t2_int_unit_i, self.t2_int_val_i)

    def update_combobox(self, combo, values):
        idx = combo.current()
        combo.config(values=values)
        if idx == -1: combo.current(1)
        else: combo.current(idx)

    def create_date_inputs(self, parent):
        entries = {}
        variables = {}
        labels = ["Thn", "Bln", "Tgl", "Jam", "Mnt", "Dtk"]
        defaults = [2025, 1, 1, 12, 0, 0]
        limits = {"Thn": (1980, 2099), "Bln": (1, 12), "Tgl": (1, 31), "Jam": (0, 23), "Mnt": (0, 59), "Dtk": (0, 59)}
        frame = tk.Frame(parent)
        frame.pack()
        def update_days(*args):
            try:
                y, m = variables["Thn"].get(), variables["Bln"].get()
                m = max(1, min(12, m))
                _, max_d = calendar.monthrange(y, m)
                entries["Tgl"].config(to=max_d)
                if variables["Tgl"].get() > max_d: variables["Tgl"].set(max_d)
            except: pass
        for i, (lbl, val) in enumerate(zip(labels, defaults)):
            f = tk.Frame(frame); f.grid(row=0, column=i, padx=2)
            tk.Label(f, text=lbl, font=("Arial", 7)).pack()
            mn, mx = limits[lbl]
            var = tk.IntVar(value=val); variables[lbl] = var
            e = tk.Spinbox(f, from_=mn, to=mx, width=4, wrap=True, textvariable=var)
            e.pack()
            entries[lbl] = e
            if lbl in ["Thn", "Bln"]: var.trace_add("write", update_days)
        update_days()
        return entries, variables

    def update_date_labels(self, entries, t, keys):
        l_map = {k: t[v] for k, v in zip(["Thn", "Bln", "Tgl", "Jam", "Mnt", "Dtk"], keys)}
        for k, w in entries.items():
            for c in w.master.winfo_children():
                if isinstance(c, tk.Label): c.config(text=l_map[k])

    def set_current_time(self, vars_dict):
        n = datetime.now()
        for k, v in zip(["Thn", "Bln", "Tgl", "Jam", "Mnt", "Dtk"], [n.year, n.month, n.day, n.hour, n.minute, n.second]):
            vars_dict[k].set(v)

    def get_date(self, vars_dict):
        try: return datetime(vars_dict["Thn"].get(), vars_dict["Bln"].get(), vars_dict["Tgl"].get(), vars_dict["Jam"].get(), vars_dict["Mnt"].get(), vars_dict["Dtk"].get())
        except: return None

    def update_interval_limit(self, combo, spinbox):
        idx = combo.current()
        limit = 23 if idx == 2 else (59 if idx < 2 else 999)
        spinbox.config(to=limit)
        try:
            if int(spinbox.get()) > limit: spinbox.delete(0, "end"); spinbox.insert(0, str(limit))
        except: pass

    def t1_browse(self):
        f = filedialog.askdirectory()
        if f: self.t1_path_var.set(f)

    def t1_toggle_cre(self):
        st = "normal" if self.t1_use_cre.get() else "disabled"
        self.t1_rb_sync.config(state=st)
        self.t1_rb_custom.config(state=st)
        self.t1_toggle_inputs()
    
    def t1_toggle_inputs(self):
        st = "normal" if self.t1_use_cre.get() and self.t1_cre_mode.get() == "custom" else "disabled"
        for w in self.t1_fr_cre_inp.winfo_children():
            if isinstance(w, tk.Button): w.config(state=st)
            else:
                for c in w.winfo_children():
                    for s in c.winfo_children(): s.config(state=st)

    def t2_toggle_cre(self):
        st = "normal" if self.t2_use_cre.get() else "disabled"
        self.t2_rb_sync.config(state=st)
        self.t2_rb_custom.config(state=st)
        self.t2_toggle_inputs()
    
    def t2_toggle_inputs(self):
        st = "normal" if self.t2_use_cre.get() and self.t2_cre_mode.get() == "custom" else "disabled"
        for w in self.t2_fr_cre_inp.winfo_children():
            if isinstance(w, tk.Button): w.config(state=st)
            else:
                for c in w.winfo_children():
                    for s in c.winfo_children(): s.config(state=st)

    def get_delta(self, val_w, unit_w):
        val = int(val_w.get())
        idx = unit_w.current()
        if idx == 0: return timedelta(seconds=val)
        if idx == 1: return timedelta(minutes=val)
        if idx == 2: return timedelta(hours=val)
        return timedelta(days=val)

    def run_shuffle_files(self):
        path = self.t1_path_var.get()
        start = self.get_date(self.t1_mod_vars)
        if not path or not os.path.exists(path): return messagebox.showerror("Err", TRANSLATIONS[self.lang_code]["msg_folder_err"])
        if not start: return messagebox.showerror("Err", TRANSLATIONS[self.lang_code]["msg_date_err"])

        exts = ('.flac', '.mp3', '.wav', '.aiff', '.m4a', '.ogg', '.wma', '.opus', '.dsd', '.dsf')
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.lower().endswith(exts): files.append(os.path.join(r, file))
        
        if not files: return messagebox.showwarning("Empty", "No files found!")
        random.shuffle(files)

        delta = self.get_delta(self.t1_int_val, self.t1_int_unit)
        curr_m = start
        curr_c = self.get_date(self.t1_cre_vars) if (self.t1_use_cre.get() and self.t1_cre_mode.get() == "custom") else start
        if not curr_c: curr_c = start

        self.status_label.config(text=TRANSLATIONS[self.lang_code]["status_working"])
        self.root.update()
        count = 0
        
        for f in files:
            os.utime(f, (curr_m.timestamp(), curr_m.timestamp()))
            if self.t1_use_cre.get():
                target = curr_m if self.t1_cre_mode.get() == "sync" else curr_c
                set_file_creation_time(f, target.timestamp())
                if self.t1_cre_mode.get() == "custom": curr_c += delta
            curr_m += delta
            count += 1
        
        self.status_label.config(text=TRANSLATIONS[self.lang_code]["status_done"])
        messagebox.showinfo("Success", TRANSLATIONS[self.lang_code]["msg_success"].format(count))

    # --- REVISED LOGIC: SYNCHRONIZED SMART INTERVAL ---
    def run_sort_folders(self):
        folders = self.folder_data
        start_mod = self.get_date(self.t2_mod_vars)
        if not folders: return messagebox.showerror("Err", TRANSLATIONS[self.lang_code]["msg_folder_err"])
        if not start_mod: return messagebox.showerror("Err", TRANSLATIONS[self.lang_code]["msg_date_err"])

        use_cre = self.t2_use_cre.get()
        cre_mode = self.t2_cre_mode.get()
        start_cre = self.get_date(self.t2_cre_vars) if (use_cre and cre_mode == "custom") else start_mod
        if not start_cre: start_cre = start_mod

        delta_folder = self.get_delta(self.t2_int_val_f, self.t2_int_unit_f)
        delta_file = self.get_delta(self.t2_int_val_i, self.t2_int_unit_i)
        
        sync_content = self.t2_sync_var.get()
        
        curr_folder_mod = start_mod
        curr_folder_cre = start_cre
        
        self.status_label.config(text=TRANSLATIONS[self.lang_code]["status_working"])
        self.root.update()
        count_folders = 0
        count_files = 0
        exts = ('.flac', '.mp3', '.wav', '.aiff', '.m4a', '.ogg', '.wma', '.opus', '.dsd', '.dsf')

        for folder in folders:
            # 1. Update Folder Time
            ts_folder_mod = curr_folder_mod.timestamp()
            ts_folder_cre = curr_folder_cre.timestamp() if use_cre else ts_folder_mod
            
            try:
                os.utime(folder, (ts_folder_mod, ts_folder_mod))
                if use_cre: set_file_creation_time(folder, ts_folder_cre)
                count_folders += 1
            except: pass
            
            # 2. Sync Content
            file_duration_total = timedelta(0)
            if sync_content:
                curr_file_mod = curr_folder_mod
                curr_file_cre = curr_folder_cre if use_cre else curr_file_mod
                
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if file.lower().endswith(exts):
                            fpath = os.path.join(root, file)
                            try:
                                ts_f_mod = curr_file_mod.timestamp()
                                os.utime(fpath, (ts_f_mod, ts_f_mod))
                                
                                ts_f_cre = curr_file_cre.timestamp() if use_cre else ts_f_mod
                                set_file_creation_time(fpath, ts_f_cre) 
                                
                                curr_file_mod += delta_file
                                if use_cre: curr_file_cre += delta_file
                                count_files += 1
                            except: pass
                
                if count_files > 0:
                    file_duration_total = curr_file_mod - curr_folder_mod

            # 3. Next Folder Time (Synchronized Smart Jump)
            target_next_mod = curr_folder_mod + delta_folder
            last_file_end_time = curr_folder_mod + file_duration_total
            
            while target_next_mod < last_file_end_time:
                target_next_mod += delta_folder 
            
            # Calculate actual jump duration
            actual_jump = target_next_mod - curr_folder_mod
            
            # Apply jump to both timelines
            curr_folder_mod = target_next_mod
            if use_cre:
                curr_folder_cre += actual_jump # Created date now jumps the exact same amount!

        self.status_label.config(text=TRANSLATIONS[self.lang_code]["status_done"])
        msg = f"Processed {count_folders} folders and {count_files} files."
        messagebox.showinfo("Success", msg)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = AudioShufflerApp(root)
    root.mainloop()