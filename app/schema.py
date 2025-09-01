import strawberry
from app.domain.user.graphql.query import UserQuery
from app.domain.user.graphql.mutation import UserMutation

@strawberry.type
class Query(UserQuery):   # merge queries
    pass

@strawberry.type
class Mutation(UserMutation):  # merge mutations
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
