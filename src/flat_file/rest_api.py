from fastapi import FastAPI, Form, HTTPException
from .flat_file_loader import Flat_file_loader
from .user import User

class Rest_api:
    def __init__(self, database_file_name: str = "db_flat_file.json"):
        self.flat_file_loader = Flat_file_loader(database_file_name)
        self.in_memory_database: dict[str, User] = {}  # gem User-instanser

        self.app = FastAPI()
        self.app.add_event_handler("startup", self.on_startup)

        # CRUD endpoints
        self.app.post("/user")(self.create_user)
        self.app.get("/user/{person_id}")(self.read_user)
        self.app.put("/user/{person_id}")(self.update_user)
        self.app.delete("/user/{person_id}")(self.delete_user)
        self.app.get("/users")(self.list_users)

    def on_startup(self):
        """Load users from file into memory as User instances"""
        data = self.flat_file_loader.load_memory_database_from_file()
        self.in_memory_database = {str(u.person_id): u for u in data}
        print(f"[Startup] Loaded {len(self.in_memory_database)} users")

    # ----------------------
    # CREATE
    # ----------------------
    def create_user(
        self,
        person_id: int = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        address: str = Form(...),
        street_number: int = Form(...),
        password: str = Form(...),
    ):
        str_id = str(person_id)
        if str_id in self.in_memory_database:
            raise HTTPException(status_code=400, detail="User findes allerede")

        user = User(
            person_id=person_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
            street_number=street_number,
            password=password,
        )
        self.in_memory_database[str_id] = user
        self.flat_file_loader.save_memory_database_to_file(self.in_memory_database.values())

        return {"header": {"status": "gemt", "code": 200}, "body": user.__dict__}

    # ----------------------
    # READ
    # ----------------------
    def read_user(self, person_id: str):
        if person_id not in self.in_memory_database:
            raise HTTPException(status_code=404, detail="User findes ikke")
        user = self.in_memory_database[person_id]
        return {"header": {"status": "ok", "code": 200}, "body": user.__dict__}

    # ----------------------
    # UPDATE
    # ----------------------
    def update_user(
        self,
        person_id: str,
        first_name: str = Form(None),
        last_name: str = Form(None),
        address: str = Form(None),
        street_number: int = Form(None),
        password: str = Form(None),
        enabled: bool = Form(None),
    ):
        if person_id not in self.in_memory_database:
            raise HTTPException(status_code=404, detail="User findes ikke")

        user = self.in_memory_database[person_id]

        # Opdater kun de felter, som er sendt
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if address is not None:
            user.address = address
        if street_number is not None:
            user.street_number = street_number
        if password is not None:
            user.password = password
        if enabled is not None:
            user.enabled = enabled

        self.flat_file_loader.save_memory_database_to_file(self.in_memory_database.values())
        return {"header": {"status": "opdateret", "code": 200}, "body": user.__dict__}

    # ----------------------
    # DELETE
    # ----------------------
    def delete_user(self, person_id: str):
        if person_id not in self.in_memory_database:
            raise HTTPException(status_code=404, detail="User findes ikke")

        user = self.in_memory_database.pop(person_id)
        self.flat_file_loader.save_memory_database_to_file(self.in_memory_database.values())
        return {"header": {"status": "slettet", "code": 200}, "body": user.__dict__}

    # ----------------------
    # LIST ALL USERS
    # ----------------------
    def list_users(self):
        users_list = [u.__dict__ for u in self.in_memory_database.values()]
        return {"header": {"status": "ok", "code": 200}, "body": users_list}
