# src/test_strategier/login_system.py

class LoginSystem:
    def __init__(self):
        self.users = {}
        self.locked_users = set()
        self.failed_attempts = {}

    def create_user(self, username, password):
        self.users[username] = password
        self.failed_attempts[username] = 0

    def login(self, username, password):
        if username in self.locked_users:
            return "låst"
        if username not in self.users:
            return "ukendt bruger"
        if self.users[username] == password:
            self.failed_attempts[username] = 0
            return "ok"
        else:
            self.failed_attempts[username] += 1
            if self.failed_attempts[username] >= 3:
                self.locked_users.add(username)
            return "forkert"