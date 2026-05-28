# Loan Aggregate Root:
# ISBN(Value Object), Book(Entity, 책), Member(Entity, 회원)을
# 하나로 묶어서 관리하는 것이 Aggregate Root이다.

# Loan (Aggregate Root)
# ├── Book  (어떤 책을?)
# ├── Member (누가?)
# └── 대출일, 반납기한, 반납여부 (언제?)

# 왜 Loan이 Aggregate Root 인가?
# '대출'없이는 Book과 Member가 연결될 수 없다.
# Book.is_available, Member.loan_count 등은 누가 바꾸나?
# 바로 Loan이 책임지고 관리한다.
# 즉 외부에서 Book이나 Member를 직접 건드리지 않고,
# 반드시 Loan을 통해서만 상태가 바뀌어야 한다.


from dataclasses import dataclass
from datetime import date, timedelta

from domain.book.book import Book
from domain.member.member import Member


@dataclass
class Loan:
    loan_id: str  # 대출 식별자
    book: Book  # Book Entity
    member: Member  # Member Entity
    loan_date: date  # 대출일
    is_returned: bool = False  # 반납 여부 (기본값 False)
    due_date: date | None = None

    # 책 반납
    def return_book(self) -> None:
        self.is_returned = True
        self.book.is_available = True
        self.member.loan_count -= 1

    # __init__이 실행된 직후 자동으로 호출되는 메서드
    def __post_init__(self) -> None:
        # __post__init__ 은 객체 초기화만 담당하고, 상태 변경은 별도 메서드로 분리하자.
        if not self.due_date:
            self.due_date = self.loan_date + timedelta(days=14)

    def start_loan(self) -> None:
        # 대출할떄만 호출하자.
        # 유효성 검사 - 책이 대출 불가능한 상태이거나 회원이 책을 대출할 수 있는 상태가 아니면 에러
        if not self.book.is_available:
            raise ValueError(
                f"책 대출 불가 - 책이 이용가능한 상태가 아님 | book:{self.book} member:{self.member}"
            )

        if not self.member.can_borrow():
            raise ValueError(
                f"책 대출 불가 - 회원이 대출 가능한 상태가 아님 | book:{self.book} member:{self.member}"
            )

        # 책을 대출하면서 상태 변경
        self.book.is_available = False
        self.member.loan_count += 1

    # 연체 여부 조회
    def is_overdue(self) -> bool:
        return date.today() > self.due_date
