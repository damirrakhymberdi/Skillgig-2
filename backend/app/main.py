from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .core.config import get_settings
from .database import Base, engine
from .migrations import run_startup_migrations
from .routers import auth, users, questions, categories, stats, chat


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Ensure tables exist on each serverless instance. A database outage should
    # not prevent the ASGI app from starting; request handlers will surface the
    # unavailable database instead of returning a platform-level invocation 500.
    try:
        Base.metadata.create_all(bind=engine)
        run_startup_migrations(engine)
    except Exception as exc:  # pragma: no cover - depends on external database
        print(f"Database startup failed: {exc}")
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


@app.get(f"{settings.api_prefix}/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except Exception as exc:  # pragma: no cover - depends on external database
        print(f"Health database check failed: {exc}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "degraded",
                "database": "unavailable",
                "error": type(exc).__name__,
            },
        )


def create_app():
    return app
