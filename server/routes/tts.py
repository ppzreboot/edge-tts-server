import io

import edge_tts
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from server.auth import verify_api_key
from server.schemas import TTSRequest

router = APIRouter(tags=["tts"])


@router.post("/tts", response_class=Response, dependencies=[Depends(verify_api_key)])
async def synthesize(req: TTSRequest) -> Response:
    communicate = edge_tts.Communicate(
        req.text,
        voice=req.voice,
        rate=req.rate,
        volume=req.volume,
        pitch=req.pitch,
    )

    audio = io.BytesIO()
    try:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.write(chunk["data"])
    except edge_tts.exceptions.NoAudioReceived:
        raise HTTPException(status_code=502, detail="no audio received from TTS service")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    data = audio.getvalue()
    if not data:
        raise HTTPException(status_code=502, detail="empty audio response")

    return Response(content=data, media_type="audio/mpeg")
