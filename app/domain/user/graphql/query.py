# app/domain/user/graphql/query.py
import strawberry
from sqlalchemy.orm import Session
from app.domain.user.models import User  # SQLAlchemy model
from .types import UserType
from strawberry.types import Info

@strawberry.type
class UserQuery:
    @strawberry.field
    def user(self, info: Info, id: int) -> UserType | None:
        db: Session = info.context["db"]
        user = db.query(User).filter(User.id == id).first()
        if not user:
            return None
        return UserType(id=user.id, name=user.name, email=user.email)
