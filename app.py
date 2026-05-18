"""Vercel 与 `python app.py` 的入口：导出 FastAPI 实例 `app`。"""

from server import create_app

app = create_app()


def main() -> None:
    import uvicorn

    from server.config import HOST, PORT

    uvicorn.run("app:app", host=HOST, port=PORT, reload=False)


if __name__ == "__main__":
    main()
