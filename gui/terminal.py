import tkinter as tk


class TerminalApp:
    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("ArdOS Terminal")
        self.window.geometry("600x400")
        self.kernel = kernel  # İşletim sistemi çekirdeğini buraya bağladık

        # Siyah Terminal Ekranı
        self.text_area = tk.Text(self.window, bg="black", fg="#00FF00", font=("Consolas", 11), insertbackground="white")
        self.text_area.pack(expand=True, fill="both")

        # İlk promptu yaz
        self.prompt = f"{self.kernel.current_user}@{self.kernel.hostname}:{self.kernel.fs.get_path_string()}$ "
        self.text_area.insert("end", self.prompt)

        # Enter tuşuna basılınca komutu işle
        self.text_area.bind("<Return>", self.process_command)

        # Kullanıcının geçmiş satırları silmesini engellemek için (Basit koruma)
        self.text_area.bind("<BackSpace>", self.protect_prompt)

    def process_command(self, event):
        # Son satırı al
        full_text = self.text_area.get("1.0", "end-1c")  # Tüm metni al
        last_line = full_text.split("\n")[-1]  # Son satırı bul

        # Prompt kısmını temizle, sadece komutu al
        command = last_line.replace(self.prompt, "").strip()

        # Kernel'e gönder ve cevabı al
        if command:
            response = self.kernel.execute_command(command)
        else:
            response = ""

        # Cevabı ekrana yaz (Yeni satıra geçtikten sonra)
        self.text_area.insert("end", "\n")

        if response == "CLEAR_SIGNAL":
            self.text_area.delete("1.0", "end")
        elif response:
            self.text_area.insert("end", response + "\n")

        # Yeni prompt hazırla
        path = self.kernel.fs.get_path_string()
        self.prompt = f"{self.kernel.current_user}@{self.kernel.hostname}:{path}$ "
        self.text_area.insert("end", self.prompt)

        # İmleci sona taşı ve scroll yap
        self.text_area.see("end")

        return "break"  # Varsayılan Enter işlemini (yeni satır eklemeyi) durdur

    def protect_prompt(self, event):
        # Kullanıcı prompt'u silmeye çalışırsa engelle (Gelişmiş versiyonlarda daha iyi yapılabilir)
        pass