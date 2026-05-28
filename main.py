from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.book_router import router as book_router
from api.loan_router import router as loan_router
from api.member_router import router as member_router
from infrastructure.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # lifespan 함수
    # - yield 전: 앱 시작시 실행 (DB 초기화 등)
    # - yield
    # - yield 후: 앱 종료 시 실행 (커넥션 정리 등)

    init_db()
    yield


app = FastAPI(lifespan=lifespan)

# main.py는 router를 연결하는 역할
app.include_router(loan_router)
app.include_router(member_router)
app.include_router(book_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
