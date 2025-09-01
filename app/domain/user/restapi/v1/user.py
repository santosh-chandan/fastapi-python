from fastapi import APIRouter, Depends, Header, Query,  Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.user import schema, models
from app.domain.user import services
from app.core.logging import logger
from app.domain.user.utils import auth
from app.core.config import settings
from typing import List
from app.core.limiter import limiter
from app.core.redis import RedisClient
import json

router = APIRouter(prefix='/v1/user', tags=['V1 Users'])

@router.post('/', response_model=schema.getUser)
def create_user(user: schema.createUser, db: Session = Depends(get_db)):
    return services.create_user(db, user)


# Here, token and db are not passed manually.
# Instead, they are resolved automatically by FastAPI’s dependency injection system.
@router.get("/me")
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# db is variable has sqlalchemy session object => db: session
# get_db => has some value which initialized session object
# Depends(get_db) => tells FastAPI: "Before running this function (get_user), call get_db() and pass its result as the value of db."
# Depends() is a special helper that tells FastAPI:
# "This argument is a dependency. Please resolve it before running the function."
@router.get('/{id}', response_model=schema.getUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return services.get_user_by_id(db, id)

# Get users list with pagination
@router.get("/users/", response_model=List[schema.getUser])
# the limiter just checks Redis synchronously under the hood. so we can keep async
@limiter.limit("5/minute")   # Limit: 5 requests per minute per IP
def read_users(
        db: Session = Depends(get_db),
        page: int = Query(settings.DEFAULT_PAGE, ge=1), # skip: int = 0, 
        page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE) # limit: int = 10, 
        ):

    cache_key = f"users:page={page}:size={page_size}"
    # 1. Try Redis cache
    cached_data = RedisClient.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # 2. Fetch from DB if not cached
    users, total = services.get_users(db, skip=page, limit=page_size)

    # Generate pagination info
    total_pages = (total + page_size - 1) // page_size  # ceil division
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    # log users
    logger.info(users)

    result = {
        "data": [user.dict() for user in users],  # Convert SQLAlchemy → dict
        "pagination": {
            "current_page": page,
            "page_size": page_size,
            "total_users": total,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page,
        },
    }

    # 3. Save in Redis with 60s TTL
    RedisClient.setex(cache_key, 60, json.dumps(result, default=str))

    return result


# form_data: OAuth2PasswordRequestForm = Depends()
# When you add this parameter in your function, FastAPI:
# Reads the incoming request.
# Extracts username and password (from form-data).
# Creates an instance of OAuth2PasswordRequestForm.
# Injects it into your function as form_data.
@router.post('/login')
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
def login(request: schema.login, 
          response: Response, 
          db: Session = Depends(get_db),
          client_type: str = Header(default="web")):
    try:
        user = services.authenticate_user(db, request)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = auth.create_access_token(data={"sub": user.id})
        refresh_token = auth.create_refresh_token({"sub": str(user.id)})

        if client_type == "web":
            # set refresh token in HTTP-only cookie
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,  # Marked as httponly=True so JS cannot read it.
                secure=True,   # only over HTTPS
                samesite="strict"
            )
        else:  # e.g. mobile client
            # Send refresh token in response body instead
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException as http_exc:
        # Reraise known HTTP exceptions (like 401)
        raise http_exc
    except Exception as e:
        logger.info({str(e)})
        logger.info("Unexpected error during login")  # Logs full traceback
        raise HTTPException(status_code=500, detail="Internal server error")

## Refresh Token
# When you log in, the backend gives you an Access Token (short-lived, e.g. 15–30 mins).
# But once it expires, the user would otherwise need to log in again with username/password.
# To avoid asking for credentials again and again, we issue a Refresh Token:
# Access Token → Short-lived, used on every request (Bearer token).
# Refresh Token → Long-lived (days or weeks), stored securely (e.g., HTTP-only cookie, secure storage in mobile app).
# When access token expires → Client calls /refresh with the refresh token → Backend validates it → Issues a new access token (and maybe new refresh token).
# This reduces password exposure and keeps sessions alive securely.
# --- REFRESH ---
@router.post("/refresh")
def refresh_token(
    response: Response,
    payload: dict = Depends(auth.verify_refresh_token),
    client_type: str = Header(default="web")
):
    new_access = auth.create_access_token({"sub": payload["sub"]})
    new_refresh = auth.create_refresh_token({"sub": payload["sub"]})

    if client_type == "web":
        # (optional) rotate the refresh token:
        # Restricts where the cookie is sent.
        # "/" means the cookie is included for all requests to your domain (any path).
        # If you set path="/refresh", the browser would only send it for /refresh endpoint requests.
        response.set_cookie(
            key="refresh_token",
            value=new_refresh,
            httponly=True,
            secure=False,       # True only with HTTPS
            samesite="strict",
            max_age= auth.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 24 * 3600,
            path="/",
        )
    else:  # e.g. mobile client
        # Send refresh token in response body instead
        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "bearer",
        }

    return {"access_token": new_access, "token_type": "bearer"}

