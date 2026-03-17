import tkinter as tk
import calendar
from datetime import datetime
from .constants import COLORS

class CalendarWidget:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Takvim")
        self.window.geometry("300x350")
        self.window.configure(bg=COLORS["bg"])

        now = datetime.now()
        self.year = now.year
        self.month = now.month

        # Başlık (Ay ve Yıl)
        header_frame = tk.Frame(self.window, bg=COLORS["taskbar"])
        header_frame.pack(fill="x")

        tk.Button(header_frame, text="<", bg=COLORS["taskbar"], fg="white", relief="flat", command=self.prev_month).pack(side="left", padx=10)
        self.month_label = tk.Label(header_frame, text="", bg=COLORS["taskbar"], fg="white", font=("Segoe UI", 12, "bold"))
        self.month_label.pack(side="left", expand=True)
        tk.Button(header_frame, text=">", bg=COLORS["taskbar"], fg="white", relief="flat", command=self.next_month).pack(side="right", padx=10)

        # Günler Tablosu
        self.calendar_frame = tk.Frame(self.window, bg=COLORS["bg"])
        self.calendar_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_calendar()

    def update_calendar(self):
        # Önceki çizimleri temizle
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

        # Gün isimleri (Pzt, Sal, ...)
        days = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, bg=COLORS["bg"], fg=COLORS["highlight"], font=("Segoe UI", 10, "bold")).grid(row=0, column=i)

        # Ayın günleri
        cal = calendar.monthcalendar(self.year, self.month)
        today = datetime.now()

        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day == 0: continue
                
                # Bugünün rengini farklı yap
                is_today = (day == today.day and self.month == today.month and self.year == today.year)
                bg_color = COLORS["highlight"] if is_today else COLORS["bg"]
                fg_color = "black" if is_today else COLORS["text"]

                tk.Label(self.calendar_frame, text=str(day), bg=bg_color, fg=fg_color, width=4, height=2,
                         font=("Segoe UI", 10)).grid(row=row_idx+1, column=col_idx)

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_calendar()
