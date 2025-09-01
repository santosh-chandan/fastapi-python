# app/domain/user/graphql/mutation.py
import strawberry
from .types import UserType
from .. import services  # import business logic layer


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str) -> UserType:
        # Step 1: call service layer
        user = services.create_user(name=name, email=email)

        # Step 2: return as GraphQL type
        return UserType(
            id=user.id,
            name=user.name,
            email=user.email,
        )
