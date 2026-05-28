import uuid
from datetime import date, timedelta

from domain.loan.loan import Loan


def test_loan_create(book, member):
    loan_id = str(uuid.uuid4())
    loan_date = date.today()

    loan = Loan(
        loan_id=loan_id,
        book=book,
        member=member,
        loan_date=loan_date,
    )

    assert loan.loan_id == loan_id
    assert loan.book == book
    assert loan.member == member
    assert loan.loan_date == loan_date
    assert loan.due_date == loan_date + timedelta(days=14)
    assert loan.is_returned is False


def test_loan_return_book(book, member):
    loan = Loan(
        loan_id=str(uuid.uuid4()),
        book=book,
        member=member,
        loan_date=date.today(),
    )

    loan.return_book()

    assert loan.is_returned is True


def test_loan_is_not_overdue(book, member):
    # 연체 아닌 경우
    loan = Loan(
        loan_id=str(uuid.uuid4()),
        book=book,
        member=member,
        loan_date=date.today(),
    )

    assert loan.is_overdue() is False


def test_loan_is_overdue(book, member):
    # 연체인 경우
    loan = Loan(
        loan_id=str(uuid.uuid4()),
        book=book,
        member=member,
        loan_date=date.today() - timedelta(days=15),
    )

    assert loan.is_overdue() is True
