import tkinter as tk
from tkinter import messagebox
from .constants import GRID_WIDTH, GRID_HEIGHT, START_OFFSET_X, START_OFFSET_Y, COLORS, FONTS


class DraggableIcon:
    def __init__(self, manager, name, icon_char, col, row, command, is_trash=False):
        self.manager = manager
        self.root = manager.root
        self.command = command
        self.name = name
        self.is_trash = is_trash
        self.selected = False  # Seçim durumu

        # Grid Konumu
        self.col = col
        self.row = row

        # Piksel Konumu
        self.start_x = START_OFFSET_X + (col * GRID_WIDTH)
        self.start_y = START_OFFSET_Y + (row * GRID_HEIGHT)

        # UI Oluştur
        self.create_widgets(name, icon_char)

        # Olayları Bağla
        self.bind_events()

        # Sürükleme Verisi
        self._drag_data = {"x": 0, "y": 0, "start_x": 0, "start_y": 0, "is_dragging": False}

        # Sisteme Kaydet
        self.manager.register_icon(self, col, row)

    def create_widgets(self, name, icon_char):
        self.frame = tk.Frame(self.root, bg=COLORS["bg"], cursor="hand2", width=60, height=70)
        self.frame.place(x=self.start_x, y=self.start_y)

        self.lbl_icon = tk.Label(self.frame, text=icon_char, bg=COLORS["bg"], fg=COLORS["text"], font=FONTS["icon"])
        self.lbl_icon.pack()

        self.lbl_name = tk.Label(self.frame, text=name, bg=COLORS["bg"], fg=COLORS["text"], font=FONTS["label"],
                                 wraplength=60)
        self.lbl_name.pack()

    def bind_events(self):
        widgets = [self.frame, self.lbl_icon, self.lbl_name]
        for w in widgets:
            w.bind("<Button-1>", self.on_click_start)
            w.bind("<B1-Motion>", self.on_drag)
            w.bind("<ButtonRelease-1>", self.on_drop)

            if self.is_trash:
                # Sağ tık (Mac ve Windows uyumlu)
                if self.root.tk.call('tk', 'windowingsystem') == 'aqua':
                    w.bind("<Button-2>", self.show_trash_menu)
                    w.bind("<Button-3>", self.show_trash_menu)
                else:
                    w.bind("<Button-3>", self.show_trash_menu)

    # --- SEÇİM FONKSİYONLARI ---
    def select(self):
        """İkonu seçili hale getirir"""
        if not self.selected:
            self.selected = True
            selection_color = "#4C566A"  # Seçim rengi
            self.frame.config(bg=selection_color)
            self.lbl_icon.config(bg=selection_color)
            self.lbl_name.config(bg=selection_color)

    def deselect(self):
        """İkon seçimini kaldırır"""
        if self.selected:
            self.selected = False
            default_bg = COLORS["bg"]
            self.frame.config(bg=default_bg)
            self.lbl_icon.config(bg=default_bg)
            self.lbl_name.config(bg=default_bg)

    # --- OLAY FONKSİYONLARI ---
    def on_click_start(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._drag_data["start_x"] = self.frame.winfo_x()
        self._drag_data["start_y"] = self.frame.winfo_y()
        self._drag_data["is_dragging"] = False
        self.frame.lift()

        # Tıklandığında seç
        self.select()

    def on_drag(self, event):
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        if abs(delta_x) > 3 or abs(delta_y) > 3:
            self._drag_data["is_dragging"] = True

        new_x = self.frame.winfo_x() + delta_x
        new_y = self.frame.winfo_y() + delta_y
        self.frame.place(x=new_x, y=new_y)

    def on_drop(self, event):
        if not self._drag_data["is_dragging"]:
            self.command()
            return

        cur_x = self.frame.winfo_x()
        cur_y = self.frame.winfo_y()

        # 1. Çöp Kutusu Kontrolü
        if not self.is_trash:
            trash = self.manager.get_trash_icon()
            if trash:
                dist = ((cur_x - trash.start_x) ** 2 + (cur_y - trash.start_y) ** 2) ** 0.5
                if dist < 50:
                    self.delete_self()
                    return

        # 2. Grid Hesaplama
        target_col = round((cur_x - START_OFFSET_X) / GRID_WIDTH)
        target_row = round((cur_y - START_OFFSET_Y) / GRID_HEIGHT)
        if target_col < 0: target_col = 0
        if target_row < 0: target_row = 0

        # 3. Çakışma Kontrolü
        if self.manager.is_slot_occupied(target_col, target_row, self):
            self.frame.place(x=self._drag_data["start_x"], y=self._drag_data["start_y"])  # Geri sek
        else:
            snap_x = START_OFFSET_X + (target_col * GRID_WIDTH)
            snap_y = START_OFFSET_Y + (target_row * GRID_HEIGHT)
            self.frame.place(x=snap_x, y=snap_y)

            self.manager.update_icon_position(self, target_col, target_row)
            self.start_x = snap_x
            self.start_y = snap_y

    def delete_self(self):
        name = self.name
        self.manager.remove_icon(self)
        self.frame.destroy()
        if hasattr(self.manager, "notifications"):
            self.manager.notifications.show("Çöp Kutusu", f"'{name}' başarıyla silindi.", type="success")

    def show_trash_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="🗑️ Çöp Kutusunu Boşalt", command=self.empty_trash_action)
        menu.post(event.x_root, event.y_root)

    def empty_trash_action(self):
        if messagebox.askyesno("Çöp Kutusu", "Kutuyu boşaltmak istediğine emin misin?"):
            self.lbl_icon.config(fg=COLORS["danger"])
            self.root.after(200, lambda: self.lbl_icon.config(fg=COLORS["text"]))
            messagebox.showinfo("Bilgi", "Temizlendi.")