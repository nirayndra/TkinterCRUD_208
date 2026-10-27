import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "nilai_siswa.db"

def run_query(sql, params=()):
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            return conn.execute(sql, params).fetchall()
    finally:
        conn.close()

def init_db():
    run_query(
        """CREATE TABLE IF NOT EXISTS praktikum 
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER NOT NULL,
        fisika INTEGER NOT NULL,
        inggris INTEGER NOT NULL,
        prediksi_fakultas TEXT NOT NULL
        )
    """)

def add_siswa(nama, biologi, fisika, inggris, prediksi):
    run_query("INSERT INTO praktikum (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) "
              "VALUES (?, ?, ?, ?, ?)",
              (nama, biologi, fisika, inggris, prediksi))

def get_siswa():
    return run_query("SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas "
                     "FROM praktikum ORDER BY nama_siswa")
                     
def prediksi_fakultas(biologi, fisika, inggris):
    if inggris >= fisika and inggris >= biologi:
        return "Bahasa"
    elif biologi >= inggris and biologi >= fisika:
        return "Kedokteran"
    elif fisika >= inggris and fisika >= biologi:
        return "Teknik"
    else:
        return "HM. Tolong dibenarkan."

init_db()
root = tk.Tk()
root.title("Prediksi Prodi")

selected_id = None  
entries = {}
for i, field in enumerate(["Nama", "Biologi", "Fisika", "Inggris"]):
    tk.Label(root, text=field).grid(row=i, column=0, padx=5, pady=4, sticky="w")
    entries[field] = tk.Entry(root, width=30)
    entries[field].grid(row=i, column=1, padx=5, pady=4)

cols = ("id", "nama", "biologi", "fisika", "inggris", "prediksi")
tree = ttk.Treeview(root, columns=cols, show="headings")
for c in cols:
    tree.heading(c, text=c.title())
    tree.column(c, width=90, anchor="center")
tree.column("id", width=40)
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

def refresh():
    tree.delete(*tree.get_children())
    for row in get_siswa():
        tree.insert("", tk.END, values=row)

def clear_form():
    global selected_id
    selected_id = None
    for e in entries.values():
        e.delete(0, tk.END)

def read_form():
    nama = entries["Nama"].get().strip()
    biologi = entries["Biologi"].get().strip()
    fisika = entries["Fisika"].get().strip()
    inggris = entries["Inggris"].get().strip()
    if not nama or not biologi or not fisika or not inggris:
        messagebox.showwarning("Data kurang", "Semua kolom harus diisi.")
        return None
    if not (biologi.isdigit() and fisika.isdigit() and inggris.isdigit()):
        messagebox.showwarning("Nilai salah", "Nilai harus berupa angka.")
        return None
    biologi, fisika, inggris = int(biologi), int(fisika), int(inggris)
    return nama, biologi, fisika, inggris, prediksi_fakultas(biologi, fisika, inggris)

def on_add():
    data = read_form()
    if data:
        add_siswa(*data)
        clear_form()
        refresh()

btns = tk.Frame(root)
btns.grid(row=4, column=0, columnspan=2, pady=4)

for text, cmd in [("Tambah dan Lihat Prediksi", on_add)]:
    tk.Button(btns, text=text, width=20, command=cmd).pack(side="left", padx=4)

refresh()
root.mainloop()