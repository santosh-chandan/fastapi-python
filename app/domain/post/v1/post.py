from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.post import schema
from app.domain.post import services
from app.core.database import get_db
from app.core.logging import logger

router = APIRouter(prefix='/post', tags=['Post'])

# Create Post
@router.post('/', response_model=schema.GetPost)
def create_post(post: schema.CreatePost, db: Session = Depends(get_db)):
    logger.info("Post Created")
    return services.create_post(db, post)

# Get Post
@router.get('/{post_id}', response_model=schema.GetPost)
def get_post(post_id:int, db: Session = Depends(get_db)):
    return services.get_post(db, post_id)
