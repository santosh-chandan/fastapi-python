from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    level = Column(Integer, nullable=False, default=0)

    # back_populates links both directions, so you can traverse:
        # From Post → User (post.owner)
        # From User → list of posts (user.posts)
    # posts is nothing just a simple attribute of User class
    post_ref = relationship("Post", back_populates="user_ref")
