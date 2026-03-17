import tkinter as tk


class TerminalApp:
    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("ArdOS Terminal")
        self.window.geometry("600x400")
        self.kernel = kernel

        # Süreç (Process) Kaydı
        self.pid = self.kernel.register_process("Terminal")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Komut Geçmişi
        self.history = []
        self.history_idx = -1

        # Siyah Terminal Ekranı
        self.text_area = tk.Text(self.window, bg="black", fg="#00FF00", font=("Consolas", 11), insertbackground="white")
        self.text_area.pack(expand=True, fill="both")

        # İlk promptu yaz
        self.prompt = f"{self.kernel.current_user}@{self.kernel.hostname}:{self.kernel.fs.get_path_string()}$ "
        self.text_area.insert("end", self.prompt)

        # Olay (Event) Bağlamaları
        self.text_area.bind("<Return>", self.process_command)
        self.text_area.bind("<Up>", self.on_up)
        self.text_area.bind("<Down>", self.on_down)
        self.text_area.bind("<Tab>", self.on_tab)
        self.text_area.bind("<BackSpace>", self.protect_prompt)

    def on_close(self):
        self.kernel.kill_process(self.pid)
        self.window.destroy()

    def get_current_input(self):
        full_text = self.text_area.get("1.0", "end-1c")
        lines = full_text.split("\n")
        if not lines: return ""
        last_line = lines[-1]
        if last_line.startswith(self.prompt):
            return last_line[len(self.prompt):]
        return ""

    def replace_input(self, new_text):
        full_text = self.text_area.get("1.0", "end-1c")
        lines = full_text.split("\n")
        
        # Son satırı bul ve prompt'tan sonrasını sil
        self.text_area.delete(f"end-1c linestart+{len(self.prompt)}c", "end")
        self.text_area.insert("end", new_text)

    def on_up(self, event):
        if not self.history: return "break"
        if self.history_idx < len(self.history) - 1:
            self.history_idx += 1
        
        cmd = self.history[len(self.history) - 1 - self.history_idx]
        self.replace_input(cmd)
        return "break"

    def on_down(self, event):
        if not self.history: return "break"
        if self.history_idx > 0:
            self.history_idx -= 1
            cmd = self.history[len(self.history) - 1 - self.history_idx]
            self.replace_input(cmd)
        elif self.history_idx == 0:
            self.history_idx = -1
            self.replace_input("")
        return "break"

    def on_tab(self, event):
        current_input = self.get_current_input()
        if not current_input: return "break"
        
        # Son kelimeyi al (tamamlanacak olan)
        parts = current_input.split()
        if not parts: return "break"
        last_word = parts[-1]
        
        # Bulunulan dizindeki dosyalarla eşleştir
        children = self.kernel.fs.current_node.children.keys()
        matches = [f for f in children if f.startswith(last_word)]
        
        if len(matches) == 1:
            # Tam eşleşme varsa tamamla
            new_input = current_input[:len(current_input)-len(last_word)] + matches[0]
            self.replace_input(new_input)
        elif len(matches) > 1:
            # Birden fazla varsa ekrana bas
            self.text_area.insert("end", "\n" + "  ".join(matches) + "\n")
            self.text_area.insert("end", self.prompt + current_input)
            self.text_area.see("end")
            
        return "break"

    def process_command(self, event):
        command = self.get_current_input().strip()

        # Geçmişe kaydet
        if command:
            if not self.history or self.history[-1] != command:
                self.history.append(command)
        self.history_idx = -1

        # Kernel'e gönder ve cevabı al
        if command:
            response = self.kernel.execute_command(command)
        else:
            response = ""

        if response == "CLEAR_SIGNAL":
            self.text_area.delete("1.0", "end")
        elif response:
            self.text_area.insert("end", "\n" + response + "\n")
        else:
            self.text_area.insert("end", "\n")

        # Yeni prompt hazırla
        path = self.kernel.fs.get_path_string()
        self.prompt = f"{self.kernel.current_user}@{self.kernel.hostname}:{path}$ "
        self.text_area.insert("end", self.prompt)

        # İmleci sona taşı ve scroll yap
        self.text_area.mark_set("insert", "end")
        self.text_area.see("end")

        return "break"  # Varsayılan Enter işlemini (yeni satır eklemeyi) durdur

    def protect_prompt(self, event):
        # Kullanıcı prompt'u silmeye çalışırsa engelle (Gelişmiş versiyonlarda daha iyi yapılabilir)
        pass