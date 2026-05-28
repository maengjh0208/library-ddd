from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from application.loan_use_case import LoanUseCase
from domain.loan.loan_service import LoanService
from infrastructure.book_repository import BookRepositoryImp
from infrastructure.database import get_session
from infrastructure.loan_repository import LoanRepositoryImp
from infrastructure.member_repository import MemberRepositoryImp

router = APIRouter(prefix="/loans", tags=["loans"])


class BorrowRequest(BaseModel):
    isbn: str
    member_id: str


def get_loan_use_case():
    return LoanUseCase(
        book_repository=BookRepositoryImp(),
        member_repository=MemberRepositoryImp(),
        loan_repository=LoanRepositoryImp(),
        loan_service=LoanService(),
    )


# POST /loans/borrow - 대출
@router.post("/borrow")
def borrow_book(
    borrow_data: BorrowRequest,
    session=Depends(get_session),
    use_case=Depends(get_loan_use_case),
):
    try:
        loan = use_case.borrow_book(
            session=session,
            isbn=borrow_data.isbn,
            member_id=borrow_data.member_id,
        )

        return {"loan_id": loan.loan_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# POST /loans/{loan_id}/return - 반납
@router.post("/{loan_id}/return")
def return_book(
    loan_id: str, session=Depends(get_session), use_case=Depends(get_loan_use_case)
):
    try:
        use_case.return_book(
            session=session,
            loan_id=loan_id,
        )

        return {"message": "반납 완료"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
