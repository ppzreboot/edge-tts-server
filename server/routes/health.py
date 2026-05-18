from fastapi import APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse

router = APIRouter(tags=["health"])

REPO_URL = "https://github.com/AAA-voc-pifa/edge-tts-server"
ROOT_MESSAGE = (
    "部署成功。\n"
    f"项目源码：{REPO_URL}\n"
)


@router.get("/", response_class=PlainTextResponse)
async def root() -> PlainTextResponse:
    return PlainTextResponse(ROOT_MESSAGE, media_type="text/plain; charset=utf-8")


@router.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
