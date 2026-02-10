from src.flat_file.user import User
from src.flat_file.flat_file_loader import Flat_file_loader

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import gc
import os


# Master-nøgle til AES – I VIRKELIGHEDEN: fra miljøvariabel!
MASTER_KEY_ENV = os.getenv("MASTER_AES_KEY")
if MASTER_KEY_ENV:
    MASTER_KEY = base64.b64decode(MASTER_KEY_ENV)
else:
    # Demo / udvikling – ALDRIG i produktion!
    MASTER_KEY = get_random_bytes(32)
    print(" Advarsel ".center(80, "="))
    print("MASTER_KEY ikke sat i miljøvariabel → bruger midlertidig nøgle!")
    print("Dette er usikkert og kun til test/lokalt udvikling!".center(80))
    print("=" * 80)


ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)  # Argon2id


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

    def encrypt_field(self, field: str) -> str:
        """Krypterer et tekstfelt med AES-256-GCM"""
        if not field:
            return ""  # eller raise ValueError, afhængig af krav
        nonce = get_random_bytes(12)
        cipher = AES.new(MASTER_KEY, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(field.encode('utf-8'))
        return base64.b64encode(nonce + ciphertext + tag).decode('utf-8')

    def decrypt_field(self, encrypted: str) -> str:
        """Dekrypterer et felt krypteret med encrypt_field()"""
        if not encrypted:
            return ""
        try:
            data = base64.b64decode(encrypted)
            if len(data) < 28:  # 12 nonce + mindst 1 byte data + 16 tag
                raise ValueError("Krypteret data er for kort")

            nonce = data[:12]
            ciphertext_tag = data[12:]
            ciphertext = ciphertext_tag[:-16]
            received_tag = ciphertext_tag[-16:]

            cipher = AES.new(MASTER_KEY, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, received_tag)
            return plaintext.decode('utf-8')

        except Exception as e:
            # I produktion: log fejlen → kast generisk fejl til brugeren
            raise ValueError("Dekryptering mislykkedes – muligvis ugyldig eller manipuleret data") from e

    def create_user(self, first_name, last_name, address, street_number, password):
        user_id = len(self.users)

        # Hash password (zero-knowledge)
        hashed_pw = ph.hash(password)

        # Krypter følsomme felter
        encrypted_first   = self.encrypt_field(first_name)
        encrypted_last    = self.encrypt_field(last_name)
        encrypted_address = self.encrypt_field(address)

        user = User(
            person_id=user_id,
            first_name=encrypted_first,
            last_name=encrypted_last,
            address=encrypted_address,
            street_number=street_number,     # ikke følsomt
            password=hashed_pw,
            enabled=True
        )

        self.users.append(user)
        self.flat_file_loader.save_memory_database_to_file(self.users)

        # Ryd midlertidige data fra hukommelsen
        del password, first_name, last_name, address
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
            return True
        except VerifyMismatchError:
            return False
        finally:
            # Ryd altid den indtastede værdi
            del provided_password
            gc.collect()

    def get_user_decrypted(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        try:
            return {
                "person_id": user.person_id,
                "first_name": self.decrypt_field(user.first_name),
                "last_name": self.decrypt_field(user.last_name),
                "address": self.decrypt_field(user.address),
                "street_number": user.street_number,
                "enabled": user.enabled
            }
        except ValueError as e:
            print(f"Advarsel: Kunne ikke dekryptere bruger {user_id}: {e}")
            return None

    # Eksempel på opdateringsmetode
    def update_first_name(self, user_id: int, new_first_name: str):
        user = self.get_user_by_id(user_id)
        if user:
            user.first_name = self.encrypt_field(new_first_name)
            self.flat_file_loader.save_memory_database_to_file(self.users)