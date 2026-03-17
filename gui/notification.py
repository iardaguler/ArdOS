import tkinter as tk
from .constants import COLORS

class NotificationManager:
    def __init__(self, root):
        self.root = root
        self.notifications = []

    def show(self, title, message, type="info"):
        """Ekranın sağ alt köşesinde şık bir bildirim gösterir"""
        notif_win = tk.Toplevel(self.root)
        notif_win.overrideredirect(True) # Pencere kenarlıklarını kaldır
        notif_win.attributes("-topmost", True) # Her zaman üstte
        
        # Renk belirleme
        bg_color = COLORS["highlight"] if type == "info" else COLORS["danger"]
        if type == "success": bg_color = COLORS["success"]
        
        frame = tk.Frame(notif_win, bg=bg_color, padx=2, pady=2)
        frame.pack(fill="both", expand=True)
        
        inner_frame = tk.Frame(frame, bg=COLORS["taskbar"], padx=15, pady=10)
        inner_frame.pack(fill="both", expand=True)

        tk.Label(inner_frame, text=title, font=("Segoe UI", 10, "bold"), 
                 bg=COLORS["taskbar"], fg=bg_color).pack(anchor="w")
        tk.Label(inner_frame, text=message, font=("Segoe UI", 9), 
                 bg=COLORS["taskbar"], fg="white", wraplength=200).pack(anchor="w", pady=(5,0))

        # Konumlandırma (Sağ alt)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Ana pencere koordinatlarını baz alalım (Masaüstü boyutu)
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()

        x = root_x + root_w - 260
        y = root_y + root_h - 100 - (len(self.notifications) * 85)
        
        notif_win.geometry(f"250x70+{x}+{y}")
        
        self.notifications.append(notif_win)
        
        # 4 saniye sonra otomatik kapat
        self.root.after(4000, lambda: self.close_notification(notif_win))

    def close_notification(self, win):
        if win in self.notifications:
            self.notifications.remove(win)
            win.destroy()
