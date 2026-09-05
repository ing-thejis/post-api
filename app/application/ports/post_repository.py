from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.post import Post

class PostRepositoryPort(ABC):
    @abstractmethod
    def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    def get_by_id(self, post_id: int) -> Optional[Post]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Post]:
        pass

    @abstractmethod
    def update(self, post: Post) -> Post:
        pass

    @abstractmethod
    def delete(self, post_id: int) -> bool:
        pass