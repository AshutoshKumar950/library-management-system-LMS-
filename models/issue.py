from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    book_id: int
    member_id: int
    issue_date: str
    return_date: Optional[str] = None
    status: str = "Issued"

