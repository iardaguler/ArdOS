import tkinter as tk
from tkinter import messagebox
from .constants import COLORS

class ArdStoreApp:
    def __init__(self, root, kernel, desktop):
        self.window = tk.Toplevel(root)
        self.window.title("ArdStore - Uygulama Merkezi")
        self.window.geometry("500x400")
        self.window.configure(bg=COLORS["bg"])
        self.kernel = kernel
        self.desktop = desktop

        # Başlık
        header = tk.Frame(self.window, bg=COLORS["highlight"], pady=10)
        header.pack(fill="x")
        tk.Label(header, text="🛍️ ArdStore: Yeni Uygulamalar Keşfedin", bg=COLORS["highlight"], fg="black", font=("Segoe UI", 12, "bold")).pack()

        # Uygulama Listesi
        self.app_frame = tk.Frame(self.window, bg=COLORS["bg"], pady=20)
        self.app_frame.pack(fill="both", expand=True)

        self.available_apps = [
            {"name": "XOX Oyunu", "icon": "❌", "desc": "Klasik Tic-Tac-Toe oyunu.", "cmd": self.install_xox},
            {"name": "Sistem Bilgisi", "icon": "ℹ️", "desc": "ArdOS donanım simülasyonu.", "cmd": self.install_sysinfo},
            {"name": "Notlar", "icon": "📌", "desc": "Hızlı yapışkan notlar.", "cmd": self.install_notes}
        ]

        self.render_apps()

    def render_apps(self):
        for app in self.available_apps:
            item = tk.Frame(self.app_frame, bg=COLORS["taskbar"], pady=10, padx=10, highlightbackground=COLORS["highlight"], highlightthickness=1)
            item.pack(fill="x", padx=20, pady=5)

            tk.Label(item, text=app["icon"], font=("Arial", 20), bg=COLORS["taskbar"], fg=COLORS["highlight"]).pack(side="left")
            
            info_frame = tk.Frame(item, bg=COLORS["taskbar"])
            info_frame.pack(side="left", padx=10)
            tk.Label(info_frame, text=app["name"], font=("Segoe UI", 10, "bold"), bg=COLORS["taskbar"], fg="white").pack(anchor="w")
            tk.Label(info_frame, text=app["desc"], font=("Segoe UI", 8), bg=COLORS["taskbar"], fg="#aaa").pack(anchor="w")

            btn_install = tk.Button(item, text="Yükle", command=app["cmd"], bg=COLORS["success"], fg="black", relief="flat", font=("Segoe UI", 9, "bold"), padx=10)
            btn_install.pack(side="right")

    # --- SİMÜLE EDİLMİŞ UYGULAMA KURULUMLARI ---

    def install_xox(self):
        # Gerçek bir kurulumda dosya indirilir/yazılır. Burada sadece ikonu masaüstüne ekliyoruz.
        self.desktop.add_app_icon("XOX Oyunu", "❌", lambda: messagebox.showinfo("XOX", "Oyun henüz geliştirme aşamasında!"))
        self.window.destroy()

    def install_sysinfo(self):
        def show_info():
            # self.window yerine self.desktop.root kullanıyoruz
            info_win = tk.Toplevel(self.desktop.root)
            info_win.title("Sistem Bilgisi")
            info_win.geometry("300x200")
            info_win.configure(bg="#2c3e50")
            text = f"ArdOS v3.1 Professional\nKernel: Python 3.x\nVFS: JSON-Linked\nKullanıcı: {self.kernel.current_user}"
            tk.Label(info_win, text=text, fg="white", bg="#2c3e50", font=("Consolas", 10), pady=30).pack()

        self.desktop.add_app_icon("Sistem Bilgisi", "ℹ️", show_info)
        self.window.destroy()

    def install_notes(self):
        self.desktop.add_app_icon("Notlar", "📌", lambda: messagebox.showinfo("Notlar", "Yapışkan notlar servisi başlatıldı."))
        self.window.destroy()
