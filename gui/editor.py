import tkinter as tk
from tkinter import messagebox, simpledialog


class TextEditorApp:
    def __init__(self, root, kernel, file_path=None):
        self.window = tk.Toplevel(root)
        self.window.title(f"Not Defteri - {file_path if file_path else 'Adsız'}")
        self.window.geometry("600x400")
        self.kernel = kernel
        self.file_path = file_path
        
        self.pid = self.kernel.register_process(f"Not Defteri - {file_path if file_path else 'Adsız'}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- ARAÇ ÇUBUĞU ---
        toolbar = tk.Frame(self.window, bg="#ECEFF4", height=30)
        toolbar.pack(fill="x")

        # Kaydet Butonu
        btn_save = tk.Button(toolbar, text="💾 Kaydet", command=self.save_file, bg="white", relief="flat")
        btn_save.pack(side="left", padx=5, pady=2)

        # Kapat Butonu
        btn_close = tk.Button(toolbar, text="❌ Kapat", command=self.on_close, bg="white", relief="flat")
        btn_close.pack(side="right", padx=5, pady=2)

        # --- YAZI ALANI ---
        self.text_area = tk.Text(self.window, bg="white", fg="black", font=("Consolas", 12), undo=True)
        self.text_area.pack(expand=True, fill="both")

        # Eğer var olan bir dosya açıldıysa, içeriğini yükle
        if self.file_path:
            self.load_content()

    def on_close(self):
        self.kernel.kill_process(self.pid)
        self.window.destroy()

    def load_content(self):
        """Dosya içeriğini çekip ekrana basar"""
        try:
            if self.file_path in self.kernel.fs.current_node.children:
                node = self.kernel.fs.current_node.children[self.file_path]
                if not node.is_dir:
                    self.text_area.insert("1.0", node.content)
            else:
                pass
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılamadı: {e}")

    def save_file(self):
        """Ekrandaki yazıyı sanal dosyaya kaydeder"""
        if not self.file_path or self.file_path == "Adsız":
            # Kullanıcıya dosya adını sor
            new_name = simpledialog.askstring("Kaydet", "Dosya adını girin:", parent=self.window)
            if not new_name:
                return # İptal edildiyse çık
            
            if "." not in new_name:
                new_name += ".txt"
            self.file_path = new_name
            # Dosyayı oluştur
            self.kernel.fs.touch(self.file_path)

        content = self.text_area.get("1.0", "end-1c")

        # Dosya sistemine yaz
        if self.file_path in self.kernel.fs.current_node.children:
            node = self.kernel.fs.current_node.children[self.file_path]
            node.content = content
            self.kernel.fs.save_to_disk() # Diske yaz
            messagebox.showinfo("Başarılı", f"'{self.file_path}' kaydedildi!")
            self.window.title(f"Not Defteri - {self.file_path}")
        else:
            # Beklenmedik bir hata (dosya touch edilmesine rağmen bulunamadıysa)
            messagebox.showerror("Hata", "Dosya kaydedilemedi!")