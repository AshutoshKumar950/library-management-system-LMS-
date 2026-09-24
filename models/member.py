from dataclasses import dataclass


@dataclass
class Member:
    name: str
    email: str = ""
    phone: str = ""
    address: str = ""
