# app/domain/user/graphql/types.py
import strawberry

# GraphQL types
@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    level: int | None = None
