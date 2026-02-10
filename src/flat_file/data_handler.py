from src.flat_file.user import User
from src.flat_file.flat_file_loader import Flat_file_loader

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import gc

# Master-nøgle til AES (I VIRKELIGHEDEN: fra os.getenv("MASTER_KEY") eller vault!)
# DEMO: genereres hver gang – IKKE sikkert i produktion!
MASTER_KEY = get_random_bytes(32)  # AES-256 nøgle

ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)  # Argon2id – juster efter din maskine

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
        
        # Hash password (til login-verifikation – GDPR-sikker)
        hashed_pw = ph.hash(password)
        
        # Ekstra: AES-256-GCM kryptering af rå-password (valgfrit ekstra lag)
        nonce = get_random_bytes(12)
        cipher = AES.new(MASTER_KEY, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(password.encode())
        encrypted_pw = base64.b64encode(nonce + ciphertext + tag).decode('utf-8')
        
        user = User(
            person_id=user_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
            street_number=street_number,
            password=hashed_pw,           # ← gem kun hash til normal brug
            enabled=True
        )
        
        # Valgfrit: gem krypteret version som ekstra attribut (hvis admin skal kunne se)
        # user.encrypted_password = encrypted_pw
        
        self.users.append(user)
        self.flat_file_loader.save_memory_database_to_file(self.users)

        # Ryd midlertidig data fra hukommelsen
        del password
        gc.collect()

    def disable_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.enabled = False
            self.flat_file_loader.save_memory_database_to_file(self.users)

    def enable_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.enabled = True
            self.flat_file_loader.save_memory_database_to_file(self.users)

    def verify_password(self, user_id: int, provided_password: str) -> bool:
        """Tjekker om indtastet password matcher det gemte hash."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        try:
            ph.verify(user.password, provided_password)
            # Ryd straks
            del provided_password
            gc.collect()
            return True
        except VerifyMismatchError:
            del provided_password
            gc.collect()
            return False

    # Eksempel på update-metode (med save)
    def update_first_name(self, user_id, new_first_name):
        user = self.get_user_by_id(user_id)
        if user:
            user.first_name = new_first_name
            self.flat_file_loader.save_memory_database_to_file(self.users)