from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Post(Base):
    """
    Post database model.
    Mapped from PHP Chapter 3: posts table.
    Fields: id, title, status (draft/published), content, user_id
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    status = Column(
        Enum("draft", "published", name="post_status"),
        nullable=False,
        default="draft",
    )
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', status='{self.status}')>"
