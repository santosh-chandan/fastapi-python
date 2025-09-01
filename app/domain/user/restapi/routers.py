from fastapi import APIRouter
from app.domain.user.restapi.v1 import user as v1_user
from app.domain.user.restapi.v2 import user as v2_user

router = APIRouter()

# include both versions here
router.include_router(v1_user.router)
router.include_router(v2_user.router)
