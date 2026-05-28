from domain.book.book import Book
from domain.book.isbn import ISBN
from domain.loan.loan_service import LoanService
from domain.member.member import Member


def test_loan_service_can_loan(book, member):
    # 책 대출 가능
    assert LoanService().can_loan(
        book=book,
        member=member,
    )


def test_loan_service_cannot_loan_by_book_available(member):
    book = Book(
        isbn=ISBN("978-89-1234-567-8"),
        title="책 제목",
        author="책 저자",
        is_available=False,
    )

    assert not LoanService().can_loan(
        book=book,
        member=member,
    )


def test_loan_service_cannot_loan_by_member_loan_count(book):
    member = Member(
        member_id="member_001",
        name="juhee",
        loan_count=3,
    )

    assert not LoanService().can_loan(
        book=book,
        member=member,
    )


def test_loan_service_cannot_loan_by_member_overdue(book):
    member = Member(
        member_id="member_001",
        name="juhee",
        is_overdue=True,
    )

    assert not LoanService().can_loan(
        book=book,
        member=member,
    )
