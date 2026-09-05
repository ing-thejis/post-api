from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.models.post import Post
from app.application.ports.post_repository import PostRepositoryPort
from app.infrastructure.database.models import PostModel

class SQLAlchemyPostRepository(PostRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: PostModel) -> Post:
        return Post(
            id=model.id,
            title=model.title,
            content=model.content,
            author_id=model.author_id
        )

    def create(self, post: Post) -> Post:
        db_post = PostModel(
            title=post.title,
            content=post.content,
            author_id=post.author_id
        )
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return self._to_domain(db_post)

    def get_by_id(self, post_id: int) -> Optional[Post]:
        db_post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        return self._to_domain(db_post) if db_post else None

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Post]:
        db_posts = self.db.query(PostModel).offset(skip).limit(limit).all()
        return [self._to_domain(p) for p in db_posts]

    def update(self, post: Post) -> Post:
        db_post = self.db.query(PostModel).filter(PostModel.id == post.id).first()
        if db_post:
            db_post.title = post.title
            db_post.content = post.content
            self.db.commit()
            self.db.refresh(db_post)
            return self._to_domain(db_post)
        return post

    def delete(self, post_id: int) -> bool:
        db_post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        if db_post:
            self.db.delete(db_post)
            self.db.commit()
            return True
        return False