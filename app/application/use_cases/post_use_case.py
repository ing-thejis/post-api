from typing import List, Optional
from app.domain.models.post import Post
from app.application.ports.post_repository import PostRepositoryPort

class PostUseCase:
    def __init__(self, post_repo: PostRepositoryPort):
        self.post_repo = post_repo

    def create_post(self, title: str, content: str, author_id: int) -> Post:
        post = Post(id=None, title=title, content=content, author_id=author_id)
        return self.post_repo.create(post)

    def get_post(self, post_id: int) -> Optional[Post]:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError("Publicación no encontrada")
        return post

    def list_posts(self, skip: int = 0, limit: int = 10) -> List[Post]:
        return self.post_repo.get_all(skip=skip, limit=limit)

    def update_post(self, post_id: int, user_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Post:
        post = self.get_post(post_id)
        if post.author_id != user_id:
            raise PermissionError("No tienes permiso para actualizar esta publicación")
        
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content

        return self.post_repo.update(post)

    def delete_post(self, post_id: int, user_id: int) -> bool:
        post = self.get_post(post_id)
        if post.author_id != user_id:
            raise PermissionError("No tienes permiso para eliminar esta publicación")
        return self.post_repo.delete(post_id)