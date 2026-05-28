from domain.member.member import Member
from domain.member.member_repository import MemberRepository


class MemberUseCase:
    def __init__(
        self,
        member_repository: MemberRepository,
    ):
        self.member_repository = member_repository

    def create_member(self, session, member_id: str, name: str) -> Member:
        member = Member(
            member_id=member_id,
            name=name,
        )

        self.member_repository.save(session, member)
        return member

    def get_member(self, session, member_id: str) -> Member:
        member = self.member_repository.find_by_id(session, member_id)

        if not member:
            raise ValueError(f"회원을 찾을 수 없음 | member_id: {member_id}")

        return member
