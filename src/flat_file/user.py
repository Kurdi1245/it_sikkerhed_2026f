from dataclasses import dataclass

@dataclass
class User:
    person_id: int
    first_name: str
    last_name: str
    address: str
    street_number: int
    password: str
    enabled: bool = True