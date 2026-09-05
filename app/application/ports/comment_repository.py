from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.comment import Comment

class CommentRepositoryPort(ABC):
    @abstractmethod
    def create(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        pass

    @abstractmethod
    def get_by_post_id(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        pass

    @abstractmethod
    def delete(self, comment_id: int) -> bool:
        pass