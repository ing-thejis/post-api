from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    email: str
    username: str
    hashed_password: str
    is_active: bool = True