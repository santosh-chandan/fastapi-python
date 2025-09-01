## Restapi Routes
from fastapi import APIRouter
from app.domain.user.restapi import routers as user_routers
from app.domain.post import routers as post_routers
from app.core.database import get_db

## Graphql Routes
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
#from app.domain.post.graphql.schema import schema as post_schema

# Rest Routes
restapi_routes = APIRouter()
restapi_routes.include_router(user_routers.router)
restapi_routes.include_router(post_routers.router)



# Mount GraphQL Routes

# GraphQL context
def get_context():
    db = next(get_db())   # create DB session
    return {"db": db}

# GraphQL context
def get_context():
    db = next(get_db())   # create DB session
    return {"db": db}

# User GraphQL router
graphql_route = GraphQLRouter(
    schema,
    context_getter=get_context,
)
