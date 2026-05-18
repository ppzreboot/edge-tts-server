import secrets

from fastapi import Header, HTTPException

from server.config import API_KEY


async def verify_api_key(
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> None:
    if not API_KEY:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing or invalid authorization")
    token = authorization.removeprefix("Bearer ").strip()
    if not secrets.compare_digest(token, API_KEY):
        raise HTTPException(status_code=401, detail="invalid API key")
