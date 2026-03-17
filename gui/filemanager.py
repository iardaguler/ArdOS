import tkinter as tk
from tkinter import messagebox
from .editor import TextEditorApp
from .constants import COLORS, FONTS  # Ortak ayarları buradan çekiyoruz


class FileManagerApp:
    """Dosya Yöneticisi Penceresi (Bilgisayarım)"""

    def __init__(self, root, kernel):
        self.window = tk.Toplevel(root)
        self.window.title("Bilgisayarım")
        self.window.geometry("700x500")
        self.window.configure(bg=COLORS["bg"])  # Pencere arka planı koyu

        self.kernel = kernel
        self.pid = self.kernel.register_process("Bilgisayarım")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.current_path_var = tk.StringVar()

        # --- ÜST PANEL (Adres Çubuğu ve Butonlar) ---
        top_frame = tk.Frame(self.window, bg=COLORS["taskbar"], height=40)
        top_frame.pack(fill="x")

        # Geri Butonu
        back_btn = tk.Button(
            top_frame,
            text="⬆ Yukarı",
            command=self.go_up,
            bg=COLORS["highlight"],
            fg="black",
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        back_btn.pack(side="left", padx=5, pady=5)

        # Adres Çubuğu
        addr_entry = tk.Entry(
            top_frame,
            textvariable=self.current_path_var,
            font=("Consolas", 10),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],  # İmleç rengi
            relief="flat",
            state="readonly"
        )
        addr_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # --- DOSYA ALANI ---
        self.content_frame = tk.Frame(self.window, bg=COLORS["bg"])
        self.content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # İlk açılışta dosyaları listele
        self.refresh_view()

    def on_close(self):
        self.kernel.kill_process(self.pid)
        self.window.destroy()

    def refresh_view(self):
        """Mevcut klasörün içeriğini ekrana çizer"""
        # Önce eski ikonları temizle
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Adres çubuğunu güncelle
        current_path = self.kernel.fs.get_path_string()
        self.current_path_var.set(current_path)
        self.window.title(f"Bilgisayarım - {current_path}")

        # Çekirdekten (Kernel) mevcut klasördeki dosyaları al
        current_node = self.kernel.fs.current_node

        if not current_node.children:
            lbl = tk.Label(self.content_frame, text="Bu klasör boş.", bg=COLORS["bg"], fg=COLORS["text"],
                           font=FONTS["label"])
            lbl.pack(pady=20)
            return

        # Dosyaları ve Klasörleri listele
        row_idx = 0
        col_idx = 0

        for name, node in current_node.children.items():
            is_dir = node.is_dir
            icon = "📁" if is_dir else "📄"
            # Renkler: Klasör sarı, Dosya mavi
            icon_color = COLORS["warning"] if is_dir else COLORS["highlight"]

            # Kapsayıcı Çerçeve (Item Frame)
            item_frame = tk.Frame(self.content_frame, bg=COLORS["bg"], width=80, height=80, cursor="hand2")
            item_frame.grid(row=row_idx, column=col_idx, padx=10, pady=10)
            item_frame.pack_propagate(False)  # Boyutun sabit kalmasını sağlar!

            # İkon
            lbl_icon = tk.Label(item_frame, text=icon, font=("Arial", 24), bg=COLORS["bg"], fg=icon_color)
            lbl_icon.pack()

            # İsim (Buradaki fg=COLORS["text"] sayesinde yazı beyaz/gri görünür)
            lbl_name = tk.Label(
                item_frame,
                text=name,
                font=("Segoe UI", 9),
                bg=COLORS["bg"],
                fg=COLORS["text"],
                wraplength=70
            )
            lbl_name.pack()

            # Tıklama olaylarını bağla
            for w in [item_frame, lbl_icon, lbl_name]:
                # Sol Tık: Klasörse gir, dosyaysa düzenle
                w.bind("<Button-1>", lambda e, n=name, d=is_dir: self.on_item_click(n, d))
                # Sağ Tık: Menü aç
                w.bind("<Button-2>" if self.window.tk.call('tk', 'windowingsystem') == 'aqua' else "<Button-3>", 
                       lambda e, n=name, d=is_dir: self.show_context_menu(e, n, d))

            # Izgara (Grid) düzeni hesaplama (Yan yana 5 ikon)
            col_idx += 1
            if col_idx > 4:
                col_idx = 0
                row_idx += 1

    def show_context_menu(self, event, name, is_dir):
        """Sağ tık menüsünü oluşturur ve gösterir"""
        menu = tk.Menu(self.window, tearoff=0, bg=COLORS["taskbar"], fg=COLORS["text"], activebackground=COLORS["highlight"])
        
        if not is_dir:
            menu.add_command(label="📝 Düzenle", command=lambda: TextEditorApp(self.window, self.kernel, name))
        
        menu.add_command(label="🗑️ Sil", command=lambda: self.delete_item(name))
        menu.add_separator()
        menu.add_command(label="ℹ️ Özellikler", command=lambda: messagebox.showinfo("Özellikler", f"Ad: {name}\nTür: {'Dizin' if is_dir else 'Dosya'}"))

        # Menüyü farenin olduğu yerde göster
        menu.tk_popup(event.x_root, event.y_root)

    def delete_item(self, name):
        """Kernel üzerinden silme işlemi yapar"""
        if messagebox.askyesno("Onay", f"'{name}' silinecek. Emin misiniz?"):
            res = self.kernel.execute_command(f"rm {name}")
            self.refresh_view()
            messagebox.showinfo("Bilgi", res)

    def on_item_click(self, name, is_dir):
        if is_dir:
            self.kernel.fs.change_dir(name)
            self.refresh_view()
        else:
            TextEditorApp(self.window, self.kernel, file_path=name)

    def go_up(self):
        """Bir üst dizine çık"""
        self.kernel.fs.change_dir("..")
        self.refresh_view()