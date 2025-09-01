from typing import Optional
from sqlalchemy.orm import Session
from strawberry.types import Info
from app.domain.user import models, schema, services
from app.domain.user.utils import auth
from app.domain.user.graphql.types import UserType

# --- RESOLVERS (bridge between GraphQL and service layer) ---

# Resolver: get user by ID
def resolve_get_user(user_id: int, info: Info) -> Optional[UserType]:
    db: Session = info.context["db"]
    user = services.get_user_by_id(db, user_id)
    return UserType.from_instance(user) if user else None


# Resolver: current logged-in user ("me")
def resolve_me(info: Info) -> Optional[UserType]:
    db: Session = info.context["db"]
    current_user: models.User = auth.get_current_user_from_context(info)  
    # 👆 You’ll need to implement this helper, e.g. decode JWT from headers
    return UserType.from_instance(current_user)


# Resolver: create a new user
def resolve_create_user(input: schema.createUser, info: Info) -> UserType:
    db: Session = info.context["db"]
    new_user = services.create_user(db, input)
    return UserType.from_instance(new_user)
