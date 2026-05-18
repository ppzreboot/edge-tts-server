import edge_tts
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from server.auth import verify_api_key
from server.prosody import prosody_summary

router = APIRouter(tags=["voices"])


@router.get("/voices", dependencies=[Depends(verify_api_key)])
async def list_voices(
    locale: str | None = Query(
        default=None,
        description="按语言区域过滤，如 zh-CN、en-US",
        examples=["zh-CN"],
    ),
) -> JSONResponse:
    try:
        voices = await edge_tts.list_voices()
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"failed to fetch voices: {exc}"
        ) from exc

    if locale:
        prefix = locale.lower()
        voices = [v for v in voices if v.get("Locale", "").lower().startswith(prefix)]

    return JSONResponse(
        {
            "prosody": prosody_summary(),
            "count": len(voices),
            "voices": voices,
        }
    )
