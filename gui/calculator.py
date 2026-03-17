import tkinter as tk
from tkinter import messagebox
from .constants import COLORS, FONTS

class CalculatorApp:
    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("Hesap Makinesi")
        self.window.geometry("300x400")
        self.window.resizable(False, False)
        self.window.configure(bg=COLORS["bg"])
        
        self.kernel = kernel
        self.pid = self.kernel.register_process("Hesap Makinesi")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        # Ekran
        display_frame = tk.Frame(self.window, bg=COLORS["taskbar"], height=60)
        display_frame.pack(fill="x", padx=10, pady=10)
        
        display_label = tk.Label(display_frame, textvariable=self.display_var, font=("Consolas", 24), 
                                 bg=COLORS["taskbar"], fg=COLORS["text"], anchor="e", padx=10)
        display_label.pack(fill="both", expand=True)

        # Butonlar
        buttons_frame = tk.Frame(self.window, bg=COLORS["bg"])
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        btns = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row, col = 0, 0
        for btn_text in btns:
            # Renkleri daha kontrastlı hale getiriyoruz
            if btn_text in "/*-+=":
                bg_color = COLORS["highlight"]
                fg_color = "black"
            elif btn_text == "C":
                bg_color = COLORS["danger"]
                fg_color = "white"
            else:
                bg_color = "#D8DEE9" # Daha açık bir gri (Nord Snow Storm)
                fg_color = "black"
            
            btn = tk.Button(buttons_frame, text=btn_text, font=("Segoe UI", 14, "bold"), 
                            bg=bg_color, fg=fg_color,
                            relief="flat", width=5, height=2,
                            activebackground="white",
                            command=lambda t=btn_text: self.on_click(t))
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
            buttons_frame.rowconfigure(i, weight=1)

    def on_close(self):
        self.kernel.kill_process(self.pid)
        self.window.destroy()

    def on_click(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")
        elif char == "=":
            try:
                # eval() kullanımı basit hesaplamalar için yeterlidir
                result = str(eval(self.expression))
                self.display_var.set(result)
                self.expression = result
            except Exception:
                messagebox.showerror("Hata", "Geçersiz işlem")
                self.expression = ""
                self.display_var.set("0")
        else:
            if self.expression == "0": self.expression = ""
            self.expression += str(char)
            self.display_var.set(self.expression)
