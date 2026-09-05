from typing import List
from app.domain.models.comment import Comment
from app.application.ports.comment_repository import CommentRepositoryPort
from app.application.ports.post_repository import PostRepositoryPort

class CommentUseCase:
    def __init__(self, comment_repo: CommentRepositoryPort, post_repo: PostRepositoryPort):
        self.comment_repo = comment_repo
        self.post_repo = post_repo

    def add_comment(self, post_id: int, author_id: int, content: str) -> Comment:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError("El post donde intentas comentar no existe")
        
        comment = Comment(id=None, content=content, post_id=post_id, author_id=author_id)
        return self.comment_repo.create(comment)

    def list_comments_by_post(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError("El post consultado no existe")
        return self.comment_repo.get_by_post_id(post_id, skip=skip, limit=limit)

    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("El comentario no existe")
        
        if comment.author_id != user_id:
            raise PermissionError("No tienes permiso para eliminar este comentario")
            
        return self.comment_repo.delete(comment_id)