import os

MAX_TEXT_LENGTH = int(os.environ.get("MAX_TEXT_LENGTH", "5000"))
API_KEY = os.environ.get("API_KEY", "")
ENABLE_DOCS = os.environ.get("ENABLE_DOCS", "").lower() in ("1", "true", "yes")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
