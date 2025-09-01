from passlib.context import CryptContext
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from app.domain.user import models

# Password hassing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# protecting routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Access Token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

# Refresh Token
# You never send username+password again, only the refresh token.
# Backend can revoke refresh tokens if needed (logout, security breach).
# Access tokens are short-lived → safer if stolen.
# Refresh tokens are long-lived but must be stored securely.
def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt

# Verify refresh token
def verify_refresh_token(token: str, scope: str = "access_token"):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if payload.get("scope") != scope:
            raise JWTError("Invalid scope")
        return payload
    except JWTError:
        return None


# Get current User
# Here, token and db are not passed manually.
# Instead, they are resolved automatically by FastAPI’s dependency injection system.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    user = db.query(models.User).filter(models.User.email == username).first()
    if user is None:
        HTTPException(status_code=401, detail="User not found")
    return user
