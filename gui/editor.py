import tkinter as tk
from tkinter import messagebox


class TextEditorApp:
    def __init__(self, root, kernel, file_path=None):
        self.window = tk.Toplevel(root)
        self.window.title(f"Not Defteri - {file_path if file_path else 'Adsız'}")
        self.window.geometry("600x400")
        self.kernel = kernel
        self.file_path = file_path

        # --- ARAÇ ÇUBUĞU ---
        toolbar = tk.Frame(self.window, bg="#ECEFF4", height=30)
        toolbar.pack(fill="x")

        # Kaydet Butonu
        btn_save = tk.Button(toolbar, text="💾 Kaydet", command=self.save_file, bg="white", relief="flat")
        btn_save.pack(side="left", padx=5, pady=2)

        # Kapat Butonu
        btn_close = tk.Button(toolbar, text="❌ Kapat", command=self.window.destroy, bg="white", relief="flat")
        btn_close.pack(side="right", padx=5, pady=2)

        # --- YAZI ALANI ---
        self.text_area = tk.Text(self.window, bg="white", fg="black", font=("Consolas", 12), undo=True)
        self.text_area.pack(expand=True, fill="both")

        # Eğer var olan bir dosya açıldıysa, içeriğini yükle
        if self.file_path:
            self.load_content()

    def load_content(self):
        """Dosya içeriğini çekip ekrana basar"""
        try:
            # Dosya sisteminden düğümü (Node) bul
            # Not: get_node diye bir fonksiyonumuz yok, manuel bulacağız
            # Şimdilik basitçe: file_path sadece dosya adı ise (aynı klasördeysek)
            if self.file_path in self.kernel.fs.current_node.children:
                node = self.kernel.fs.current_node.children[self.file_path]
                if not node.is_dir:
                    self.text_area.insert("1.0", node.content)
            else:
                # Tam yol verilmişse (ileride geliştirilebilir)
                pass
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılamadı: {e}")

    def save_file(self):
        """Ekrandaki yazıyı sanal dosyaya kaydeder"""
        if not self.file_path:
            # Eğer yeni dosyaysa adını sor (Basitçe 'Adsız.txt' yapalım şimdilik)
            self.file_path = "Adsız.txt"
            # Dosyayı oluştur
            self.kernel.fs.touch(self.file_path)

        content = self.text_area.get("1.0", "end-1c")  # Son karakteri (newline) alma

        # Dosya sistemine yaz
        if self.file_path in self.kernel.fs.current_node.children:
            node = self.kernel.fs.current_node.children[self.file_path]
            node.content = content  # <-- RAM'e kaydediyoruz
            messagebox.showinfo("Başarılı", "Dosya kaydedildi!")
        else:
            # Dosya yoksa oluştur ve yaz
            self.kernel.fs.touch(self.file_path)
            node = self.kernel.fs.current_node.children[self.file_path]
            node.content = content
            messagebox.showinfo("Başarılı", "Yeni dosya oluşturuldu ve kaydedildi!")
            self.window.title(f"Not Defteri - {self.file_path}")