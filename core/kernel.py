import os
import time
import getpass
from datetime import datetime

# --- DÜZELTİLEN IMPORT KISIMLARI ---
# core klasöründeki filesytem.py dosyasından VirtualFileSystem sınıfını çek
# Paket içinden doğru şekilde import etmek için relative import kullanın.
from .filesytem import VirtualFileSystem
from .auth import AuthManager

class ArdOS:
    def __init__(self):
        self.fs = VirtualFileSystem()
        self.auth = AuthManager()
        self.hostname = "ardos-pro"
        self.is_running = True
        self.current_user = None

        # Varsayılan klasörleri oluştur
        self.fs.mkdir("home")
        self.fs.mkdir("bin")
        self.fs.mkdir("etc")

    def boot(self):
        self.clear_screen()
        print("\n" + "=" * 50)
        print("   A R D O S   P R O F E S S I O N A L   v 2.1")
        print("=" * 50)
        time.sleep(1)
        self.login()

    def login(self):
        print("Authentication Required.")
        while True:
            username = input("Login: ").strip()
            password = getpass.getpass("Password: ").strip()

            if self.auth.check_login(username, password):
                self.current_user = username
                print(f"\nWelcome to ArdOS, {username}.\n")
                self.run()
                break
            else:
                print("Access Denied.")

    def clear_screen(self):
        # Windows ve Mac/Linux uyumlu ekran temizleme
        os.system('cls' if os.name == 'nt' else 'clear')

    def execute_command(self, cmd_str):
        if not cmd_str: return
        parts = cmd_str.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            print("Commands: ls, mkdir, touch, cd, whoami, date, clear, exit")
        elif cmd == "ls":
            print(self.fs.list_dir())
        elif cmd == "mkdir" and args:
            print(self.fs.mkdir(args[0]))
        elif cmd == "touch" and args:
            print(self.fs.touch(args[0]))
        elif cmd == "cd" and args:
            res = self.fs.change_dir(args[0])
            if res: print(res)
        elif cmd == "whoami":
            print(self.current_user)
        elif cmd == "date":
            print(datetime.now().ctime())
        elif cmd == "clear":
            self.clear_screen()
        elif cmd == "exit":
            self.is_running = False
        else:
            print(f"Unknown command: {cmd}")

    def run(self):
        while self.is_running:
            path = self.fs.get_path_string()
            # Renkli Prompt (Terminal destekliyorsa renkli görünür)
            prompt = f"\033[92m{self.current_user}@{self.hostname}\033[0m:\033[94m{path}\033[0m$ "
            try:
                command = input(prompt).strip()
                self.execute_command(command)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")