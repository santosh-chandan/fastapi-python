from fastapi import APIRouter
from app.domain.post.v1 import post as v1_post


router = APIRouter()
router.include_router(v1_post.router)
