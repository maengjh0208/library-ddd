from dataclasses import dataclass

# 비즈니스 규칙
# 1. 최대 3권까지 대출 가능
# 2. 연체 중이면 대출 불가


@dataclass
class Member:
    member_id: str  # 회원 식별자
    name: str  # 회원 이름
    loan_count: int = 0  # 현재 대출 권수 (default 0)
    is_overdue: bool = False  # 연체 여부 (default False)

    def can_borrow(self) -> bool:
        return self.loan_count < 3 and not self.is_overdue

    def __eq__(self, other) -> bool:
        if not isinstance(other, Member):
            return False

        return self.member_id == other.member_id

    def __hash__(self) -> int:
        return hash(self.member_id)
