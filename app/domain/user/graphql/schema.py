import strawberry
from app.domain.user.graphql.types import UserType
from app.domain.user.graphql.resolvers import resolve_get_user, resolve_me, resolve_create_user

@strawberry.type
class Query:
    user: UserType | None = strawberry.field(resolver=resolve_get_user)
    me: UserType | None = strawberry.field(resolver=resolve_me)

@strawberry.type
class Mutation:
    create_user: UserType = strawberry.mutation(resolver=resolve_create_user)

schema = strawberry.Schema(query=Query, mutation=Mutation)
