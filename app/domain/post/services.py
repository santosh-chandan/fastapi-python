from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.domain.post import schema, models

# Create Post
def create_post(db: Session, post:schema.CreatePost):
    db_post = db.query(models.Post).filter(models.Post.title == post.title).first()
    if db_post:
        raise HTTPException(status_code=404, detail="post alreay exist.")
    new_post = models.Post(
        title = post.title,
        content = post.content,
        user_id = 1
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get Post
def get_post(db:Session, id:int):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


