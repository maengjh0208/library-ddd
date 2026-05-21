from sqlalchemy import select

from domain.member import Member
from domain.member_repository import MemberRepository
from infrastructure.models import MemberModel


class MemberRepositoryImp(MemberRepository):
    def find_by_id(self, session, member_id: str) -> Member | None:
        query = select(
            MemberModel.member_id,
            MemberModel.name,
            MemberModel.loan_count,
            MemberModel.is_overdue,
        ).where(MemberModel.member_id == member_id)

        row = session.execute(query).one_or_none()

        return (
            Member(
                member_id=row.member_id,
                name=row.name,
                loan_count=row.loan_count,
                is_overdue=row.is_overdue,
            )
            if row
            else None
        )

    def save(self, session, member: Member) -> None:
        model = MemberModel(
            member_id=member.member_id,
            name=member.name,
            loan_count=member.loan_count,
            is_overdue=member.is_overdue,
        )

        session.merge(model)
