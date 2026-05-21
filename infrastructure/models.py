from sqlalchemy import Boolean, Column, Integer, String

from infrastructure.database import Base


class BookModel(Base):
    __tablename__ = "books"

    isbn = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)


class MemberModel(Base):
    __tablename__ = "members"

    member_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    loan_count = Column(Integer, default=0)
    is_overdue = Column(Boolean, default=False)
