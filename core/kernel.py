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

        # Süreç Yönetimi (Process Management)
        self.processes = {}
        self.next_pid = 1000

        # Diski yükle
        self.fs.load_from_disk()
        
        # Varsayılan sistem klasörlerini oluştur (Yoksa)
        if not self.fs.root.children:
            self.fs.mkdir("home")
            self.fs.mkdir("bin")
            self.fs.mkdir("etc")
            self.fs.mkdir("var")
            
        # Log klasörünü zorla oluştur
        self.execute_command("mkdir var")
        self.execute_command("mkdir var/log")

    def log_event(self, message):
        """Sistem olaylarını /var/log/syslog dosyasına kaydeder"""
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_line = f"{timestamp} {message}\n"
        
        # Basit bir append (sonuna ekleme) mantığı
        # Gerçekte VFS'de append fonksiyonu olmalı ama şimdilik mevcut içeriği alıp üstüne ekliyoruz
        syslog = self.fs.read_file("syslog")
        if "Error" in syslog: # Dosya yoksa
            syslog = ""
            
        # Eğer log dosyası çok büyürse sondan 50 satırı tut
        lines = syslog.split("\n")
        if len(lines) > 50:
            syslog = "\n".join(lines[-50:])
            
        new_content = syslog + log_line
        
        # Geçici olarak dizin değiştirip yazalım
        current_path = self.fs.get_path_string()
        self.fs.current_node = self.fs.root
        
        # var/log içine gir
        if "var" in self.fs.root.children:
            self.fs.current_node = self.fs.root.children["var"]
            if "log" in self.fs.current_node.children:
                self.fs.current_node = self.fs.current_node.children["log"]
                
                # Dosyayı oluştur veya güncelle
                if "syslog" not in self.fs.current_node.children:
                    self.fs.touch("syslog")
                self.fs.current_node.children["syslog"].content = new_content
        
        # Eski dizine dön
        self.fs.change_dir("/")
        for folder in [f for f in current_path.split("/") if f]:
            self.fs.change_dir(folder)

    def register_process(self, name):
        """Yeni bir uygulama açıldığında PID verir"""
        pid = self.next_pid
        self.processes[pid] = name
        self.next_pid += 1
        self.log_event(f"PROCESS START: {name} [PID: {pid}]")
        return pid

    def kill_process(self, pid):
        """Uygulamayı sonlandırır (Kayıtlardan siler)"""
        if pid in self.processes:
            name = self.processes.pop(pid)
            self.log_event(f"PROCESS KILL: {name} [PID: {pid}]")
            return True
        return False

    def boot(self):
        self.clear_screen()
        print("\n" + "=" * 50)
        print("   A R D O S   P R O F E S S I O N A L   v 3.1")
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
                self.log_event(f"LOGIN SUCCESS: User '{username}' logged in.")
                print(f"\nWelcome to ArdOS, {username}.\n")
                self.run()
                break
            else:
                self.log_event(f"LOGIN FAILED: Attempt for user '{username}' failed.")
                print("Access Denied.")

    def clear_screen(self):
        # Windows ve Mac/Linux uyumlu ekran temizleme
        os.system('cls' if os.name == 'nt' else 'clear')

    def execute_command(self, cmd_str):
        if not cmd_str: return ""
        
        self.log_event(f"COMMAND [{self.current_user}]: {cmd_str}")

        # Basit Pipe (|) ve Grep Desteği
        pipe_cmd = None
        if "|" in cmd_str:
            parts = cmd_str.split("|", 1)
            cmd_str = parts[0].strip()
            pipe_cmd = parts[1].strip()

        parts = cmd_str.split()
        cmd = parts[0].lower()
        args = parts[1:]

        response = ""
        
        # Sudo Desteği (Yetki Yükseltme)
        if cmd == "sudo":
            if not args: return "Usage: sudo <command>"
            if self.current_user not in ["root", "admin"]:
                return f"{self.current_user} is not in the sudoers file. This incident will be reported."
            
            # Geçici olarak root ol
            old_user = self.current_user
            self.current_user = "root"
            # Kalan komutu tekrar çalıştır
            sub_cmd = " ".join(args)
            if pipe_cmd: sub_cmd += f" | {pipe_cmd}"
            response = self.execute_command(sub_cmd)
            # Yetkiyi geri al
            self.current_user = old_user
            return response

        if cmd == "help":
            response = "Commands: ls [-a], mkdir, touch, cd, cat, rm, whoami, date, sudo, clear, exit\nHint: You can use '| grep <text>' with any command."
        elif cmd == "ls":
            show_all = "-a" in args
            response = self.fs.list_dir(show_all=show_all)
        elif cmd == "mkdir":
            if args:
                response = self.fs.mkdir(args[0], user=self.current_user)
            else:
                response = "Usage: mkdir <directory_name>"
        elif cmd == "touch":
            if args:
                response = self.fs.touch(args[0], user=self.current_user)
            else:
                response = "Usage: touch <file_name>"
        elif cmd == "cd":
            if args:
                res = self.fs.change_dir(args[0])
                response = res if res else ""
            else:
                response = ""
        elif cmd == "cat":
            if args:
                response = self.fs.read_file(args[0], user=self.current_user)
            else:
                response = "Usage: cat <file_name>"
        elif cmd == "rm":
            if args:
                response = self.fs.remove(args[0], user=self.current_user)
            else:
                response = "Usage: rm <name>"
        elif cmd == "whoami":
            response = str(self.current_user)
        elif cmd == "date":
            response = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif cmd == "clear":
            response = "CLEAR_SIGNAL"
        elif cmd == "exit":
            self.is_running = False
            response = "System shutting down..."
        else:
            response = f"Unknown command: {cmd}"

        # Grep Filtreleme
        if pipe_cmd and pipe_cmd.startswith("grep "):
            search_term = pipe_cmd.split(" ", 1)[1]
            lines = response.split("\n")
            matched_lines = [line for line in lines if search_term in line]
            response = "\n".join(matched_lines)

        # Her komuttan sonra diski kaydet
        self.fs.save_to_disk()
        return response

    def run(self):
        while self.is_running:
            path = self.fs.get_path_string()
            # Renkli Prompt (Terminal destekliyorsa renkli görünür)
            prompt = f"\033[92m{self.current_user}@{self.hostname}\033[0m:\033[94m{path}\033[0m$ "
            try:
                command = input(prompt).strip()
                output = self.execute_command(command)
                if output == "CLEAR_SIGNAL":
                    self.clear_screen()
                elif output:
                    print(output)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")