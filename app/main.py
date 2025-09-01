from fastapi import FastAPI
from app import routes
from app.core.database import Base, engine
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter, rate_limit_exceeded_handler

# app = FastAPI(title="FastAPI")


# What happens here?
# When the app starts:
# Everything before yield runs (startup logic).
# Example: create tables, connect to DB, load configs, etc.
# yield → tells FastAPI "okay, go ahead and start serving requests".
# When the app shuts down:
# Everything after yield runs (shutdown logic).
# Example: close DB connections, cleanup resources, etc.
# Create tables automatically on startup


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     Base.metadata.create_all(bind=engine)
#     yield
#     # Shutdown (if needed, e.g., close connections)

# # Create app with lifespan handler
# app = FastAPI(title="FastAPI Blog", lifespan=lifespan)


app = FastAPI(title="FastAPI Blog")

# Attach limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# All Routers
app.include_router(routes.restapi_routes, prefix="/api")
app.include_router(routes.graphql_route, prefix="/graphql")

# Root Router
@app.get('/', tags=['Root'])
def root():
    return {"Welcome to Blog Module."}
