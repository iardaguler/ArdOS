import tkinter as tk
from tkinter import messagebox, simpledialog
from .constants import COLORS

class UserManagerApp:
    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("Kullanıcı Yönetimi")
        self.window.geometry("400x300")
        self.window.configure(bg=COLORS["bg"])
        self.kernel = kernel
        
        self.pid = self.kernel.register_process("Kullanıcı Yönetimi")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        tk.Label(self.window, text="Kayıtlı Kullanıcılar", bg=COLORS["bg"], fg="white", font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Liste kutusunu daha okunaklı bir arka plan ile güncelliyoruz
        self.user_listbox = tk.Listbox(self.window, bg="#D8DEE9", fg="black", font=("Segoe UI", 10, "bold"), relief="flat")
        self.user_listbox.pack(fill="both", expand=True, padx=20, pady=5)

        btn_frame = tk.Frame(self.window, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="➕ Ekle", command=self.add_user, bg=COLORS["success"], fg="black", relief="flat", width=12, font=("Segoe UI", 9, "bold")).pack(side="left", padx=25)
        tk.Button(btn_frame, text="🗑️ Sil", command=self.remove_user, bg=COLORS["danger"], fg="white", relief="flat", width=12, font=("Segoe UI", 9, "bold")).pack(side="right", padx=25)

        self.refresh_users()

    def on_close(self):
        self.kernel.kill_process(self.pid)
        self.window.destroy()

    def refresh_users(self):
        self.user_listbox.delete(0, "end")
        for user in self.kernel.auth.users:
            self.user_listbox.insert("end", f"👤 {user}")

    def add_user(self):
        new_user = simpledialog.askstring("Yeni Kullanıcı", "Kullanıcı adı:", parent=self.window)
        if not new_user: return
        new_pass = simpledialog.askstring("Yeni Kullanıcı", "Şifre:", parent=self.window, show="*")
        if not new_pass: return

        success, msg = self.kernel.auth.add_user(new_user, new_pass)
        messagebox.showinfo("Bilgi", msg)
        self.refresh_users()

    def remove_user(self):
        selected = self.user_listbox.get(tk.ACTIVE)
        if not selected: return
        username = selected.replace("👤 ", "")
        
        if messagebox.askyesno("Onay", f"'{username}' kullanıcısını silmek istediğinize emin misiniz?"):
            success, msg = self.kernel.auth.remove_user(username)
            messagebox.showinfo("Bilgi", msg)
            self.refresh_users()
