from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    """
    Comment database model.
    Mapped from PHP Chapter 3: comments table.
    Fields: id, comment, post_id, user_id
    """

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Relationships
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"
