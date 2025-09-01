from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from app.core.database import get_db
from app.domain.user import schema
from app.domain.user import services
from app.core.logging import logger

router = APIRouter(prefix='/v2/user', tags=['V2 Users'])

# Override: v2 create_user adds "is_active=True" by default
@router.post('/', response_model=schema.getUser)
def create_user(user: schema.createUser, db: session = Depends(get_db)):

    # model_dump() does the same thing: returns a dictionary with all field values.
    # It also has more control with options like exclude, include
    # user.model_dump(exclude={"password"})
    user_data = user.model_dump()
    user_data["level"] = 1
    # schemas.CreateUser(**user_data) takes that dictionary and passes it as keyword arguments into the Pydantic model constructor.
    # Behind the scenes, it runs validation again to ensure that all the fields match the schema definition.

    # Both are same
    # schemas.CreateUser(**{"username": "santosh", "email": "x@y.com", "is_active": True})
    # schemas.CreateUser(username="santosh", email="x@y.com", is_active=True)
    return services.create_user(db, schema.createUser(**user_data))
