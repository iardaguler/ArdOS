import json
import os

class AuthManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = {
            "admin": "admin",
            "arda": "1234"
        }
        self.load_users()

    def load_users(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.users = json.load(f)
            except:
                pass

    def save_users(self):
        with open(self.filename, "w") as f:
            json.dump(self.users, f, indent=4)

    def check_login(self, username, password):
        """Kullanıcı adı ve şifreyi doğrular"""
        if username in self.users and self.users[username] == password:
            return True
        return False

    def add_user(self, username, password):
        if username in self.users:
            return False, "Kullanıcı zaten mevcut!"
        self.users[username] = password
        self.save_users()
        return True, f"Kullanıcı '{username}' başarıyla eklendi."

    def remove_user(self, username):
        if username == "admin":
            return False, "Admin kullanıcısı silinemez!"
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True, f"Kullanıcı '{username}' silindi."
        return False, "Kullanıcı bulunamadı."