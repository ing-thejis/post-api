from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.models.comment import Comment
from app.application.ports.comment_repository import CommentRepositoryPort
from app.infrastructure.database.models import CommentModel

class SQLAlchemyCommentRepository(CommentRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            content=model.content,
            post_id=model.post_id,
            author_id=model.author_id
        )

    def create(self, comment: Comment) -> Comment:
        db_comment = CommentModel(
            content=comment.content,
            post_id=comment.post_id,
            author_id=comment.author_id
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return self._to_domain(db_comment)

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        db_comment = self.db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        return self._to_domain(db_comment) if db_comment else None

    def get_by_post_id(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        db_comments = (
            self.db.query(CommentModel)
            .filter(CommentModel.post_id == post_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(c) for c in db_comments]

    def delete(self, comment_id: int) -> bool:
        db_comment = self.db.query(CommentModel).filter(CommentModel.id == comment_id).first()
        if db_comment:
            self.db.delete(db_comment)
            self.db.commit()
            return True
        return False