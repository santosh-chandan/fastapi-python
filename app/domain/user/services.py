from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.domain.user import models
from app.domain.user import schema
from app.domain.user.utils.auth import hash_password, verify_password
from app.core.logging import logger
from typing import List, Tuple
from app.core.config import settings

# User Services
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    # optional helper used by "me" resolver if you want to fetch by email
    def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()

# create user
def create_user(db: Session, user: schema.createUser):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exist.")
    
    hash_pwd = hash_password(user.password)
    new_user = models.User(
        name = user.name,
        email = user.email,
        level = user.level,
        password = hash_pwd
    )
    db.add(new_user) # → stage object in session.
    db.commit() # → flush changes → commit transaction → write to DB.
    db.refresh(new_user) # → pull latest DB values back into the object.

    return new_user

# Join in sqlalchemy
# db.query(User).join(Post, User.id == Post.owner_id).filter(Post.id == 1).first()
def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist.")
    return db_user


# skip: How many records to skip (used for pagination, e.g., page 2 skips first 10 users).
# limit: Max number of users to return per request.
# -> List[models.User]: Type hint, says this function returns a list of User objects.
def get_users(
        db: Session, 
        page: int = settings.DEFAULT_PAGE,
        page_size: int = settings.DEFAULT_PAGE_SIZE
    ) -> Tuple[List[models.User], int]:
    """
    Args:
        db (Session): SQLAlchemy database session
        skip (int): Number of records to skip (for pagination)
        limit (int): Maximum number of records to return
    Returns:
        List[User]: List of user objects
    """
    total_users = db.query(models.User).count()
    users = db.query(models.User).offset(page).limit(page_size).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    
    return users, total_users

# Authenticate User
def authenticate_user(db: Session, request:schema.login):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    # user.__dict__ if user else "User not found"
    if not user or not verify_password(request.password, user.password):
        return None

    return user
