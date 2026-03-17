import tkinter as tk
from tkinter import messagebox
from .constants import COLORS

class TaskManagerApp:
    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("Görev Yöneticisi")
        self.window.geometry("400x350")
        self.window.configure(bg=COLORS["bg"])
        self.kernel = kernel
        
        self.pid = self.kernel.register_process("Görev Yöneticisi")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        tk.Label(self.window, text="Çalışan İşlemler (Processes)", bg=COLORS["bg"], fg="white", font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Liste kutusu
        self.process_listbox = tk.Listbox(self.window, bg="#D8DEE9", fg="black", font=("Consolas", 10, "bold"), relief="flat")
        self.process_listbox.pack(fill="both", expand=True, padx=20, pady=5)

        # Butonlar
        btn_frame = tk.Frame(self.window, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="🔄 Yenile", command=self.refresh_list, bg=COLORS["highlight"], fg="black", relief="flat", width=12, font=("Segoe UI", 9, "bold")).pack(side="left", padx=25)
        tk.Button(btn_frame, text="🛑 Görevi Sonlandır", command=self.kill_process, bg=COLORS["danger"], fg="white", relief="flat", width=16, font=("Segoe UI", 9, "bold")).pack(side="right", padx=25)

        self.refresh_list()

    def on_close(self):
        self.kernel.kill_process(self.pid)
        self.window.destroy()

    def refresh_list(self):
        self.process_listbox.delete(0, "end")
        for pid, name in self.kernel.processes.items():
            self.process_listbox.insert("end", f"[{pid}] - {name}")

    def kill_process(self):
        selected = self.process_listbox.get(tk.ACTIVE)
        if not selected: return
        
        # Seçili satırdan PID'yi ayıkla (Örn: "[1001] - TerminalApp")
        try:
            pid_str = selected.split("]")[0].replace("[", "")
            pid = int(pid_str)
            
            if messagebox.askyesno("Uyarı", f"PID {pid} sonlandırılacak. Emin misiniz?"):
                if self.kernel.kill_process(pid):
                    messagebox.showinfo("Bilgi", "İşlem sonlandırıldı (Not: GUI penceresi kapanmaz, sadece Kernel kaydı silinir).")
                    self.refresh_list()
                else:
                    messagebox.showerror("Hata", "İşlem bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"PID okunamadı: {e}")
