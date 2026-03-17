import tkinter as tk
from tkinter import messagebox
from .constants import COLORS

class MediaPlayerApp:
    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("ArdOS Medya Oynatıcı")
        self.window.geometry("400x450")
        self.window.configure(bg="#1e1e1e") # Koyu tema
        self.kernel = kernel
        
        self.pid = self.kernel.register_process("Medya Oynatıcı")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Albüm Kapak Resmi (Simülasyon)
        self.cover_art = tk.Label(self.window, text="🎵", font=("Arial", 80), bg="#2c3e50", fg=COLORS["highlight"])
        self.cover_art.pack(fill="x", pady=20, padx=40)

        self.track_name = tk.Label(self.window, text="Bir parça seçin...", bg="#1e1e1e", fg=COLORS["highlight"], font=("Segoe UI", 12, "bold"))
        self.track_name.pack(pady=5)

        # Şarkı Sözü / İçerik Alanı
        self.lyrics_area = tk.Text(self.window, bg="black", fg="#A3BE8C", font=("Consolas", 11), height=8, relief="flat", padx=10, pady=10)
        self.lyrics_area.pack(fill="both", expand=True, padx=20, pady=10)

        # Kontrol Butonları
        ctrl_frame = tk.Frame(self.window, bg="#1e1e1e")
        ctrl_frame.pack(fill="x", pady=10)

        tk.Button(ctrl_frame, text="📁 Aç", command=self.open_file, bg=COLORS["highlight"], fg="black", font=("Segoe UI", 9, "bold"), relief="flat", width=8).pack(side="left", padx=20)
        tk.Button(ctrl_frame, text="▶ Oynat", command=lambda: messagebox.showinfo("Bilgi", "Oynatılıyor..."), bg=COLORS["success"], fg="black", font=("Segoe UI", 9, "bold"), relief="flat", width=8).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="⏸ Durdur", command=lambda: messagebox.showinfo("Bilgi", "Durduruldu."), bg=COLORS["warning"], fg="black", font=("Segoe UI", 9, "bold"), relief="flat", width=8).pack(side="left", padx=5)

    def on_close(self):
        self.kernel.kill_process(self.pid)
        self.window.destroy()

    def open_file(self):
        # Basitçe mevcut klasördeki .txt dosyalarını medya dosyası gibi kabul edelim
        current_node = self.kernel.fs.current_node
        files = [n for n, node in current_node.children.items() if not node.is_dir]
        
        if not files:
            messagebox.showwarning("Hata", "Bu klasörde oynatılacak dosya yok.")
            return

        # Dosya seçme penceresi (Listbox ile)
        select_win = tk.Toplevel(self.window)
        select_win.title("Dosya Seç")
        lb = tk.Listbox(select_win, width=40)
        lb.pack()
        for f in files: lb.insert("end", f)
        
        def select():
            f = lb.get(tk.ACTIVE)
            if f:
                self.track_name.config(text=f)
                self.lyrics_area.delete("1.0", "end")
                self.lyrics_area.insert("end", self.kernel.fs.read_file(f))
                select_win.destroy()
        
        tk.Button(select_win, text="Seç", command=select).pack()
