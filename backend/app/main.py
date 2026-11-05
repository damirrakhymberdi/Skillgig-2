from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .database import Base, engine
from .migrations import run_startup_migrations
from .routers import auth, users, questions, categories, stats, chat


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Ensure tables exist (for SQLite/local dev)
    Base.metadata.create_all(bind=engine)
    run_startup_migrations(engine)
    yield


app = FastAPI(title=settings.app_name, openapi_url=f"{settings.api_prefix}/openapi.json")

# CORS
# - development: allow all (easy local dev)
# - production: restrict to configured origins (+ optional regex for preview URLs)
is_development = settings.environment.lower() == "development"
allow_origins = ["*"] if is_development else settings.cors_origin_list
allow_credentials = False if allow_origins == ["*"] else True
allow_origin_regex = None if is_development else settings.cors_origin_regex

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(questions.router, prefix=settings.api_prefix)
app.include_router(categories.router, prefix=settings.api_prefix)
app.include_router(stats.router, prefix=settings.api_prefix)
app.include_router(chat.router, prefix=settings.api_prefix)


@app.get("/")
def read_root():
    return {"status": "ok"}


def create_app():
    return app
