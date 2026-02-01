import tkinter as tk
from tkinter import messagebox

# Kendi modüllerimizi çağırıyoruz
from .constants import COLORS
from .taskbar import Taskbar
from .icon import DraggableIcon

# Uygulamalar
from .terminal import TerminalApp
from .filemanager import FileManagerApp
from .editor import TextEditorApp


class DesktopManager:
    def __init__(self, root, kernel):
        self.root = root
        self.kernel = kernel

        # Pencere Ayarları
        self.root.title("ArdOS Desktop Environment v3.1 (Professional)")
        self.root.geometry("1024x768")

        # --- ARKA PLAN (Canvas) ---
        # Düz renk yerine Canvas kullanıyoruz ki üzerine çizim yapabilelim.
        self.background = tk.Canvas(self.root, bg=COLORS["bg"], highlightthickness=0)
        self.background.pack(fill="both", expand=True)

        # Arka plan olaylarını bağla (Seçim kutusu için)
        self.background.bind("<Button-1>", self.on_bg_click_start)
        self.background.bind("<B1-Motion>", self.on_bg_drag)
        self.background.bind("<ButtonRelease-1>", self.on_bg_drop)

        # Seçim kutusu değişkenleri
        self.selection_rect = None
        self.sel_start_x = 0
        self.sel_start_y = 0

        # Grid Haritası ve İkon Listesi
        self.grid_map = {}
        self.icons = []

        # Bileşenleri Yükle (Taskbar en alta gelecek şekilde pack edilecek)
        self.taskbar = Taskbar(self.root, self.open_menu)
        # Taskbar'ı diğer her şeyin üstüne çıkar
        self.taskbar.lift()

        self.setup_icons()

    # --- SEÇİM KUTUSU (Rubberband Selection) ---

    def on_bg_click_start(self, event):
        """Boş alana tıklandığında"""
        # 1. Mevcut seçimleri kaldır
        self.deselect_all_icons()

        # 2. Başlangıç noktasını kaydet
        self.sel_start_x = event.x
        self.sel_start_y = event.y

        # 3. Mavi, kesik çizgili bir dikdörtgen oluştur (Henüz boyutu 0)
        # Not: Tkinter'da yarı saydam dolgu (fill) çok zordur,
        # bu yüzden profesyonel görünen kesik çizgili (dash) bir çerçeve kullanıyoruz.
        self.selection_rect = self.background.create_rectangle(
            self.sel_start_x, self.sel_start_y, self.sel_start_x, self.sel_start_y,
            outline=COLORS["highlight"],  # Mavi renk
            width=2,
            dash=(4, 4)  # Kesik çizgi efekti
        )

    def on_bg_drag(self, event):
        """Sürüklerken kutuyu yeniden boyutlandır"""
        if self.selection_rect:
            self.background.coords(self.selection_rect,
                                   self.sel_start_x, self.sel_start_y,
                                   event.x, event.y)

    def on_bg_drop(self, event):
        """Bırakıldığında seçimleri yap ve kutuyu sil"""
        if self.selection_rect:
            # Kutunun son koordinatlarını al
            x1, y1, x2, y2 = self.background.coords(self.selection_rect)

            # Koordinatları düzenle (x1 her zaman sol, y1 her zaman üst olsun)
            rx1, rx2 = min(x1, x2), max(x1, x2)
            ry1, ry2 = min(y1, y2), max(y1, y2)

            # Hangi ikonlar bu kutunun içinde kalıyor?
            for icon in self.icons:
                # İkonun orta noktasını bul (Yaklaşık)
                ix = icon.start_x + 30  # Genişlik / 2
                iy = icon.start_y + 35  # Yükseklik / 2

                # Eğer ikonun ortası kutunun içindeyse seç
                if rx1 < ix < rx2 and ry1 < iy < ry2:
                    icon.select()

            # Kutuyu tuvalden sil
            self.background.delete(self.selection_rect)
            self.selection_rect = None

    def deselect_all_icons(self):
        """Tüm ikonların seçimini kaldırır"""
        for icon in self.icons:
            icon.deselect()

    # --- DİĞER FONKSİYONLAR ---

    def setup_icons(self):
        """Masaüstü ikonlarını tanımla"""
        # (Manager, İsim, Emoji, Sütun, Satır, Komut, Çöp mü?)

        DraggableIcon(self, "Bilgisayarım", "💻", 0, 0, self.open_my_computer)
        DraggableIcon(self, "Terminal", "⌨️", 0, 1, self.open_terminal)
        DraggableIcon(self, "Not Defteri", "📝", 0, 2, lambda: TextEditorApp(self.root, self.kernel))

        # --- DEĞİŞİKLİK BURADA ---
        # Çöp Kutusu: Satır 4'ten 3'e alındı (Daha yukarı)
        DraggableIcon(self, "Çöp Kutusu", "🗑️", 0, 3, lambda: None, is_trash=True)

        DraggableIcon(self, "İnternet", "🌐", 1, 0, lambda: messagebox.showinfo("Hata", "Ağ yok."))

    # --- YÖNETİCİ FONKSİYONLARI ---

    def register_icon(self, icon, col, row):
        self.icons.append(icon)
        self.grid_map[(col, row)] = icon
        # İkonlar Tuval'in (background) üzerine yerleşmeli
        icon.frame.lift()

    def update_icon_position(self, icon, new_col, new_row):
        old_pos = (icon.col, icon.row)
        if old_pos in self.grid_map and self.grid_map[old_pos] == icon:
            del self.grid_map[old_pos]

        icon.col = new_col
        icon.row = new_row
        self.grid_map[(new_col, new_row)] = icon

    def remove_icon(self, icon):
        pos = (icon.col, icon.row)
        if pos in self.grid_map: del self.grid_map[pos]
        if icon in self.icons: self.icons.remove(icon)

    def is_slot_occupied(self, col, row, current_icon):
        if (col, row) in self.grid_map:
            return self.grid_map[(col, row)] != current_icon
        return False

    def get_trash_icon(self):
        for icon in self.icons:
            if icon.is_trash: return icon
        return None

    # --- UYGULAMALAR ---

    def open_terminal(self):
        TerminalApp(self.root, self.kernel)

    def open_my_computer(self):
        FileManagerApp(self.root, self.kernel)

    def open_menu(self):
        pass