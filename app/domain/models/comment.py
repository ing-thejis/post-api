# domain/models/comment.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Comment:
    id: Optional[int]
    content: str
    post_id: int
    author_id: int