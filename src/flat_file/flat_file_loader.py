import os
import json
from dataclasses import asdict
from src.flat_file.user import User

class Flat_file_loader:
    def __init__(self, database_file_name: str = "db_flat_file.json"):
        self.database_file_name = database_file_name

    def load_memory_database_from_file(self):
        if not os.path.exists(self.database_file_name):
            return []

        try:
            with open(self.database_file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                users_data = data.get("users", [])
                return [User(**user_dict) for user_dict in users_data]
        except Exception as e:
            print(f"WARNING: could not load {self.database_file_name}: {e}")
            return []

    def save_memory_database_to_file(self, users):
        serializable_db = {"users": [asdict(user) for user in users]}
        with open(self.database_file_name, "w", encoding="utf-8") as f:
            json.dump(serializable_db, f, indent=2, ensure_ascii=False)