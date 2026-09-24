from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    isbn: str = ""
    category: str = ""
    quantity: int = 1

