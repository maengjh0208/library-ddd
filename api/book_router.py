from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from application.book_use_case import BookUseCase
from infrastructure.book_repository import BookRepositoryImp
from infrastructure.database import get_session

router = APIRouter(prefix="/books", tags=["books"])


class BookRequest(BaseModel):
    isbn: str
    title: str
    author: str


def get_book_use_case():
    return BookUseCase(
        book_repository=BookRepositoryImp(),
    )


# POST /books - 책 등록
@router.post("")
def create_book(
    book_request: BookRequest,
    session=Depends(get_session),
    use_case=Depends(get_book_use_case),
):
    try:
        book = use_case.create_book(
            session=session,
            isbn=book_request.isbn,
            title=book_request.title,
            author=book_request.author,
        )

        return {"book": book}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# GET /books/{isbn} - 책 조회
@router.get("/{isbn}")
def get_book(
    isbn: str, session=Depends(get_session), use_case=Depends(get_book_use_case)
):
    try:
        book = use_case.get_book(
            session=session,
            isbn=isbn,
        )

        return {"book": book}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
