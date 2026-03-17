import tkinter as tk
from core.kernel import ArdOS
from gui.desktop import DesktopManager
from gui.constants import COLORS
import time

class ArdOS_System:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ArdOS Professional v3.1")
        self.root.geometry("1024x768")
        self.root.configure(bg=COLORS["bg"])
        
        # Kernel ve Sistem Başlatma
        self.kernel = ArdOS()
        
        # Başlangıçta Splash (Açılış) Ekranını Göster
        self.show_splash()
        
        self.root.mainloop()

    def show_splash(self):
        """GUI Açılış Ekranı"""
        self.splash_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.splash_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        logo_label = tk.Label(self.splash_frame, text="ArdOS", font=("Segoe UI", 64, "bold"), 
                              bg=COLORS["bg"], fg=COLORS["highlight"])
        logo_label.pack(pady=20)

        sub_text = tk.Label(self.splash_frame, text="Professional Operating System", 
                            font=("Segoe UI", 12), bg=COLORS["bg"], fg="white")
        sub_text.pack()

        # Yükleme Çubuğu (Simüle edilmiş)
        self.progress_canvas = tk.Canvas(self.splash_frame, width=400, height=10, bg="#1a1a1a", highlightthickness=0)
        self.progress_canvas.pack(pady=40)
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 10, fill=COLORS["highlight"], width=0)

        self.status_label = tk.Label(self.splash_frame, text="Sistem yükleniyor...", bg=COLORS["bg"], fg="#888")
        self.status_label.pack()

        self.update_progress(0)

    def update_progress(self, val):
        if val <= 400:
            self.progress_canvas.coords(self.progress_bar, 0, 0, val, 10)
            
            # Yükleme metinleri
            if val < 100: self.status_label.config(text="Kernel yükleniyor...")
            elif val < 250: self.status_label.config(text="VFS Mount ediliyor...")
            else: self.status_label.config(text="Sistem bileşenleri hazır.")
            
            self.root.after(20, lambda: self.update_progress(val + 4))
        else:
            self.root.after(500, self.show_login)

    def show_login(self):
        """GUI Giriş Ekranı"""
        self.splash_frame.destroy()
        
        self.login_frame = tk.Frame(self.root, bg="#3B4252", padx=40, pady=40, highlightbackground=COLORS["highlight"], highlightthickness=2)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="Giriş Yap", font=("Segoe UI", 20, "bold"), bg="#3B4252", fg="white").pack(pady=(0,20))

        tk.Label(self.login_frame, text="Kullanıcı Adı:", bg="#3B4252", fg="white").pack(anchor="w")
        self.user_ent = tk.Entry(self.login_frame, font=("Segoe UI", 12), bg="#2E3440", fg="white", insertbackground="white", relief="flat")
        self.user_ent.pack(pady=(5,15), fill="x")
        self.user_ent.insert(0, "admin") # Varsayılan

        tk.Label(self.login_frame, text="Şifre:", bg="#3B4252", fg="white").pack(anchor="w")
        self.pass_ent = tk.Entry(self.login_frame, show="*", font=("Segoe UI", 12), bg="#2E3440", fg="white", insertbackground="white", relief="flat")
        self.pass_ent.pack(pady=(5,25), fill="x")

        login_btn = tk.Button(self.login_frame, text="Sistemi Başlat", command=self.attempt_login, 
                              bg=COLORS["highlight"], fg="black", font=("Segoe UI", 12, "bold"), relief="flat", pady=10)
        login_btn.pack(fill="x")

        self.error_label = tk.Label(self.login_frame, text="", bg="#3B4252", fg=COLORS["danger"])
        self.error_label.pack(pady=10)

    def attempt_login(self):
        user = self.user_ent.get()
        pwd = self.pass_ent.get()

        if self.kernel.auth.check_login(user, pwd):
            self.kernel.current_user = user
            self.start_desktop()
        else:
            self.error_label.config(text="Hatalı kullanıcı adı veya şifre!")

    def start_desktop(self):
        self.login_frame.destroy()
        # Masaüstü Yöneticisini Başlat
        DesktopManager(self.root, self.kernel)

if __name__ == "__main__":
    ArdOS_System()
