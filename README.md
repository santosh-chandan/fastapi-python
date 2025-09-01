BlogAPI/
│── requirements.txt       # Dependencies for the project
│── .env                   # Environment variables (DB_URL, SECRET_KEY, etc.)
│── alembic.ini            # Alembic migrations config (if using SQLAlchemy)
│── README.md              # Documentation
│── app/
│    │── __init__.py
│    │── main.py           # FastAPI entry point
│    │── core/             # Core utilities
│    │   │── config.py
│    │   │── database.py
│    │   │── security.py
│    │   │── auth.py
│    │   │── cache.py
│    │   │── limiter.py
│    │   │── mail.py
│    │
│    │── blog/             # Blog module
│    │   │── __init__.py
│    │   │── models.py
│    │   │── schemas.py
│    │   │── crud.py
│    │   │── routes.py
│    │
│    │── user/             # User module
│    │   │── __init__.py
│    │   │── models.py
│    │   │── schemas.py
│    │   │── crud.py
│    │   │── routes.py
│    │
│    │── utils/            # Optional helpers
│        │── __init__.py
│        │── common.py
│
│── tests/                 # Pytest unit/integration tests
│    │── test_blog.py
│    │── test_user.py
