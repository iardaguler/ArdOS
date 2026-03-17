import tkinter as tk
import requests
import threading
from .constants import COLORS

class BrowserApp:
    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("ArdBrowser v1.0")
        self.window.geometry("800x600")
        self.window.configure(bg=COLORS["bg"])
        self.kernel = kernel

        # Adres Çubuğu
        top_frame = tk.Frame(self.window, bg=COLORS["taskbar"], pady=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="🌐 URL:", bg=COLORS["taskbar"], fg="white").pack(side="left", padx=10)
        self.url_ent = tk.Entry(top_frame, bg=COLORS["bg"], fg="white", insertbackground="white", relief="flat", font=("Segoe UI", 10))
        self.url_ent.pack(side="left", fill="x", expand=True, padx=5)
        self.url_ent.insert(0, "https://www.google.com")
        self.url_ent.bind("<Return>", lambda e: self.load_page())

        btn_go = tk.Button(top_frame, text="Git", command=self.load_page, bg=COLORS["highlight"], relief="flat", padx=10)
        btn_go.pack(side="left", padx=10)

        # İçerik Alanı
        self.content_area = tk.Text(self.window, bg="white", fg="black", font=("Consolas", 10), padx=20, pady=20)
        self.content_area.pack(fill="both", expand=True)
        
        # Başlangıç sayfasını yükle
        self.load_page()

    def load_page(self):
        url = self.url_ent.get()
        if not url.startswith("http"):
            url = "https://" + url
            self.url_ent.delete(0, "end")
            self.url_ent.insert(0, url)

        self.content_area.delete("1.0", "end")
        self.content_area.insert("end", f"[{url}] Sayfası yükleniyor...\nLütfen bekleyin...")

        # Ayrı thread'de sayfayı çek (Pencere donmasın)
        threading.Thread(target=self._fetch_url, args=(url,), daemon=True).start()

    def _fetch_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ArdOS/3.1'}
            response = requests.get(url, headers=headers, timeout=10)
            
            # HTML etiketlerini ayıklamak yerine şimdilik basit bir text/lite rendering yapalım
            # (Gerçek HTML rendering Tkinter'da çok zordur, bu yüzden saf metin basıyoruz)
            content = response.text
            
            # Sadece okunabilirliği artırmak için bir temizlik
            self.window.after(0, lambda: self.render_content(content))
        except Exception as e:
            self.window.after(0, lambda: self.content_area.insert("end", f"\n\n[!] Hata: Sayfaya ulaşılamadı.\n{e}"))

    def render_content(self, text):
        self.content_area.delete("1.0", "end")
        self.content_area.insert("end", text[:10000]) # Çok uzunsa ilk 10k karakteri bas
        self.content_area.see("1.0")
