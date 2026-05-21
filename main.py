from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    lifespan 함수
    - yield 전: 앱 시작시 실행 (DB 초기화 등)
    - yield
    - yield 후: 앱 종료 시 실행 (커넥션 정리 등)
    """
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def health_check():
    return {"status": "ok"}
