from unittest.mock import Mock

import pytest

from application.loan_use_case import LoanUseCase
from domain.book.book import Book
from domain.book.isbn import ISBN
from domain.loan.loan_service import LoanService
from domain.member.member import Member


# 정상 대출
def test_loan_use_case_borrow_book(book, member):
    # Mock은 진짜 객체 대신 쓰는 가짜 객체
    book_repository = Mock()
    # find_by_isbn 함수가 호출되면 book을 반환(return_value)하자.
    # 인자가 뭐가 됐든 상관 없이 해당 함수가 호출되면 아래에서 설정한 book을 반환한다.
    book_repository.find_by_isbn.return_value = book
    # Mock은 기본적으로 None을 반환한다. 따라서 아래는 생략 가능하다.
    # book_repository.save.return_value = None

    member_repository = Mock()
    member_repository.find_by_id.return_value = member
    # member_repository.save.return_value = None

    loan_repository = Mock()
    # loan_repository.save.return_value = None

    use_case = LoanUseCase(
        book_repository=book_repository,
        member_repository=member_repository,
        loan_repository=loan_repository,
        loan_service=LoanService(),
    )

    loan = use_case.borrow_book(
        session=Mock(),
        isbn=book.isbn.value,
        member_id=member.member_id,
    )

    assert loan.book == book
    assert loan.member == member


def test_loan_use_case_borrow_book_not_found_book(book, member):
    book_repository = Mock()
    book_repository.find_by_isbn.return_value = (
        None  # Mock 은 기본값이 None 이어서, 사실 생략해도 됨
    )

    member_repository = Mock()
    loan_repository = Mock()

    use_case = LoanUseCase(
        book_repository=book_repository,
        member_repository=member_repository,
        loan_repository=loan_repository,
        loan_service=LoanService(),
    )

    with pytest.raises(ValueError):
        use_case.borrow_book(
            session=Mock(),
            isbn=book.isbn.value,
            member_id=member.member_id,
        )


def test_loan_use_case_borrow_book_not_found_member(book, member):
    book_repository = Mock()

    member_repository = Mock()
    member_repository.find_by_id.return_value = None

    loan_repository = Mock()

    use_case = LoanUseCase(
        book_repository=book_repository,
        member_repository=member_repository,
        loan_repository=loan_repository,
        loan_service=LoanService(),
    )

    with pytest.raises(ValueError):
        use_case.borrow_book(
            session=Mock(),
            isbn=book.isbn.value,
            member_id=member.member_id,
        )


def test_loan_use_case_borrow_book_cannot_loan_state():
    book = Book(
        isbn=ISBN("978-89-1234-567-8"),
        title="책 제목",
        author="책 저자",
        is_available=False,
    )

    member = Member(
        member_id="member_001",
        name="juhee",
        loan_count=3,
        is_overdue=True,
    )

    book_repository = Mock()
    book_repository.find_by_isbn.return_value = book

    member_repository = Mock()
    member_repository.find_by_id.return_value = member

    loan_repository = Mock()

    use_case = LoanUseCase(
        book_repository=book_repository,
        member_repository=member_repository,
        loan_repository=loan_repository,
        loan_service=LoanService(),
    )

    with pytest.raises(ValueError):
        use_case.borrow_book(
            session=Mock(),
            isbn=book.isbn.value,
            member_id=member.member_id,
        )
