from domain.book.book import Book
from domain.member.member import Member


class LoanService:
    def can_loan(self, book: Book, member: Member) -> bool:
        # 조건 1 - 책이 대출 가능한 상태인가?
        # 조건 2 - 회원이 대출 가능한 상태인가?
        return book.is_available and member.can_borrow()
