# domain/models/post.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Post:
    id: Optional[int]
    title: str
    content: str
    author_id: int

