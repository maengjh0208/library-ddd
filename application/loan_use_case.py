# 대출 (borrow_book)
# 1. ISBN으로 책 조회
# 2. member_id로 회원 조회
# 3. LoanService로 대출 가능 여부 확인
# 4. Loan 생성 (Loan.__post_init__에서 book, member 상태 자동 변경)
# 5. book, member DB에 저장

# 반납 (return_book)
# 1. loan_id로 대출 조회 (일단 메모리에서)
# 2. 반납 처리 (Loan.return_book()으로 book, member 상태 자동 변경)
# 3. book, member DB에 저장


import uuid
from datetime import date

from domain.book.book_repository import BookRepository
from domain.book.isbn import ISBN
from domain.loan.loan import Loan
from domain.loan.loan_repository import LoanRepository
from domain.loan.loan_service import LoanService
from domain.member.member_repository import MemberRepository


class LoanUseCase:
    def __init__(
        self,
        book_repository: BookRepository,
        member_repository: MemberRepository,
        loan_repository: LoanRepository,
        loan_service: LoanService,
    ):
        self.book_repository = book_repository
        self.member_repository = member_repository
        self.loan_repository = loan_repository
        self.loan_service = loan_service

    def borrow_book(self, session, isbn: str, member_id: str) -> Loan:
        # isbn 을 ISBN 객체로 넘겨주는게 좋다. 왜냐? ISBN(isbn) 하면서 유효성 검사도 자동으로 됨
        book = self.book_repository.find_by_isbn(session, ISBN(isbn))

        if not book:
            raise ValueError(f"책을 찾을 수 없음 | isbn: {isbn}")

        member = self.member_repository.find_by_id(session, member_id)

        if not member:
            raise ValueError(f"회원이 존재하지 않음 | member_id: {member_id}")

        if not self.loan_service.can_loan(book, member):
            raise ValueError("책 대출 가능한 상태가 아님")

        loan = Loan(
            loan_id=str(uuid.uuid4()), book=book, member=member, loan_date=date.today()
        )
        loan.start_loan()

        self.book_repository.save(session, book)
        self.member_repository.save(session, member)
        self.loan_repository.save(session, loan)

        return loan

    def return_book(self, session, loan_id: str) -> None:
        loan = self.loan_repository.find_by_id(session, loan_id)

        if not loan:
            raise ValueError(f"대출 기록이 없음 | loan_id: {loan_id}")

        # 이미 대출 완료
        if loan.is_returned:
            raise ValueError(f"이미 반납 완료 | loan_id: {loan_id}")

        # book, member 상태 변경
        loan.return_book()

        # DB 저장
        self.book_repository.save(session, loan.book)
        self.member_repository.save(session, loan.member)
        self.loan_repository.save(session, loan)
