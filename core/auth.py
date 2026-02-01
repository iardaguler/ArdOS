class AuthManager:
    def __init__(self):
        # Kullanıcı veritabanı
        self.users = {
            "root": "toor",
            "admin": "admin",
            "arda": "1234"
        }

    def check_login(self, username, password):
        """Kullanıcı adı ve şifreyi doğrular"""
        if username in self.users and self.users[username] == password:
            return True
        return False