import sys
from core.kernel import ArdOS


def main():
    # 1. Önce İşletim Sistemi Çekirdeğini (Kernel) Başlat
    system_kernel = ArdOS()

    print("ArdOS v2.3 Bootloader")
    print("1. CLI Mode")
    print("2. GUI Mode")
    choice = input("Select: ")

    if choice == "1":
        system_kernel.boot()  # Eski usul
    elif choice == "2":
        # GUI'yi başlatırken Kernel'i parametre olarak gönderiyoruz!
        import tkinter as tk
        from gui.desktop import DesktopManager

        # Kernel'de login işlemi yapılmış gibi varsayalım veya GUI içinde login yaptıralım
        # Şimdilik direkt admin olarak açıyoruz:
        system_kernel.current_user = "admin"

        root = tk.Tk()
        app = DesktopManager(root, system_kernel)  # <--- BAĞLANTI BURADA
        root.mainloop()


if __name__ == "__main__":
    main()