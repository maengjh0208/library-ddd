from sqlalchemy import select

from domain.book import Book
from domain.isbn import ISBN
from domain.loan import Loan
from domain.loan_repository import LoanRepository
from domain.member import Member
from infrastructure.models import BookModel, LoanModel, MemberModel


class LoanRepositoryImp(LoanRepository):
    def find_by_id(self, session, loan_id: str) -> Loan | None:
        query = (
            select(
                LoanModel.loan_id,
                LoanModel.loan_date,
                LoanModel.is_returned,
                LoanModel.due_date,
                BookModel.isbn,
                BookModel.title,
                BookModel.author,
                BookModel.is_available,
                MemberModel.member_id,
                MemberModel.name,
                MemberModel.loan_count,
                MemberModel.is_overdue,
            )
            .join(BookModel, LoanModel.isbn == BookModel.isbn)
            .join(MemberModel, LoanModel.member_id == MemberModel.member_id)
            .where(LoanModel.loan_id == loan_id)
        )

        row = session.execute(query).one_or_none()

        if row is None:
            return None

        book = Book(
            isbn=ISBN(row.isbn),
            title=row.title,
            author=row.author,
            is_available=row.is_available,
        )

        member = Member(
            member_id=row.member_id,
            name=row.name,
            loan_count=row.loan_count,
            is_overdue=row.is_overdue,
        )

        return Loan(
            loan_id=row.loan_id,
            book=book,
            member=member,
            loan_date=row.loan_date,
            is_returned=row.is_returned,
            due_date=row.due_date,
        )

    def save(self, session, loan: Loan) -> None:
        model = LoanModel(
            loan_id=loan.loan_id,
            isbn=loan.book.isbn.value,
            member_id=loan.member.member_id,
            loan_date=loan.loan_date,
            due_date=loan.due_date,
            is_returned=loan.is_returned,
        )

        session.merge(model)
