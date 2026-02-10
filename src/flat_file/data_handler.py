from src.flat_file.user import User
from src.flat_file.flat_file_loader import Flat_file_loader

class Data_handler:
    def __init__(self, flat_file_name="db_flat_file.json"):
        self.flat_file_loader = Flat_file_loader(flat_file_name)
        self.users = self.flat_file_loader.load_memory_database_from_file()

    def get_number_of_users(self):
        return len(self.users)

    def get_user_by_id(self, user_id: int):
        for user in self.users:
            if user.person_id == user_id:
                return user
        return None

    def create_user(self, first_name, last_name, address, street_number, password):
        user_id = len(self.users)
        user = User(user_id, first_name, last_name, address, street_number, password)
        self.users.append(user)
        self.flat_file_loader.save_memory_database_to_file(self.users)

    def disable_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.enabled = False
            self.flat_file_loader.save_memory_database_to_file(self.users)   # ← vigtigt!

    def enable_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.enabled = True
            self.flat_file_loader.save_memory_database_to_file(self.users)   # ← vigtigt!

    # De øvrige update-metoder kan følge samme mønster hvis du vil have persistens
    def update_first_name(self, user_id, new_first_name):
        user = self.get_user_by_id(user_id)
        if user:
            user.first_name = new_first_name
            self.flat_file_loader.save_memory_database_to_file(self.users)