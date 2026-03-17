import tkinter as tk
import requests
import threading
from .constants import COLORS

class WeatherWidget:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Hava Durumu")
        self.window.geometry("250x150")
        self.window.configure(bg=COLORS["bg"])
        self.window.resizable(False, False)

        self.label_city = tk.Label(self.window, text="İstanbul", font=("Segoe UI", 12, "bold"), bg=COLORS["bg"], fg="white")
        self.label_city.pack(pady=(10, 0))

        self.label_temp = tk.Label(self.window, text="--°C", font=("Segoe UI", 24, "bold"), bg=COLORS["bg"], fg=COLORS["highlight"])
        self.label_temp.pack()

        self.label_desc = tk.Label(self.window, text="Veri alınıyor...", font=("Segoe UI", 9), bg=COLORS["bg"], fg="#888")
        self.label_desc.pack()

        # İnternet isteği arayüzü dondurmasın diye ayrı bir Thread'de çalıştırıyoruz
        threading.Thread(target=self.get_weather, daemon=True).start()

    def get_weather(self):
        try:
            # Ücretsiz ve anahtarsız Open-Meteo API (İstanbul Koordinatları)
            url = "https://api.open-meteo.com/v1/forecast?latitude=41.0082&longitude=28.9784&current_weather=true"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            temp = data["current_weather"]["temperature"]
            
            self.label_temp.config(text=f"{temp}°C")
            self.label_desc.config(text="Durum: Açık / Bulutlu", fg=COLORS["success"])
        except Exception as e:
            self.label_desc.config(text="Bağlantı Hatası!", fg=COLORS["danger"])
