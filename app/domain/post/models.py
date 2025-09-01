from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    # relationship("User", back_populates="posts") does NOT change the table schema.
    # It adds a Python-level object relationship so you can navigate between objects without writing manual JOINs.
    user_ref = relationship("User", back_populates="post_ref")  # Many-to-one
