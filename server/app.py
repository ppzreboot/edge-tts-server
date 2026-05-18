from fastapi import FastAPI

from server.config import ENABLE_DOCS
from server.routes import health_router, tts_router, voices_router


def _docs_url(path: str) -> str | None:
    return path if ENABLE_DOCS else None


def create_app() -> FastAPI:
    app = FastAPI(
        title="edge-tts-server",
        docs_url=_docs_url("/docs"),
        redoc_url=_docs_url("/redoc"),
        openapi_url=_docs_url("/openapi.json"),
    )
    app.include_router(health_router)
    app.include_router(voices_router)
    app.include_router(tts_router)
    return app
