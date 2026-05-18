from server.routes.health import router as health_router
from server.routes.tts import router as tts_router
from server.routes.voices import router as voices_router

__all__ = ["health_router", "voices_router", "tts_router"]
