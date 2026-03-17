import tkinter as tk
import time
from .constants import COLORS, FONTS
from .calendar_widget import CalendarWidget


class Taskbar(tk.Frame):
    def __init__(self, master, menu_command):
        super().__init__(master, bg=COLORS["taskbar"], height=45)
        self.pack(side="bottom", fill="x")
        self.pack_propagate(False)

        self.menu_command = menu_command
        self.setup_widgets()

    def setup_widgets(self):
        # Başlat Butonu
        btn = tk.Button(
            self,
            text=" ◍ ArdOS ",
            bg=COLORS["highlight"],
            fg="black",
            font=FONTS["start_btn"],
            relief="flat",
            command=self.menu_command
        )
        btn.pack(side="left", padx=10, pady=7)

        # Saat
        self.clock_lbl = tk.Label(self, text="00:00", bg=COLORS["taskbar"], fg=COLORS["text"], font=FONTS["clock"], cursor="hand2")
        self.clock_lbl.pack(side="right", padx=15)
        self.clock_lbl.bind("<Button-1>", lambda e: CalendarWidget(self.master))
        self.update_clock()

    def update_clock(self):
        self.clock_lbl.config(text=time.strftime("%H:%M"))
        self.after(1000, self.update_clock)