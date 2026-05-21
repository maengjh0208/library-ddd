from sqlalchemy import select

from domain.book import Book
from domain.book_repository import BookRepository
from domain.isbn import ISBN
from infrastructure.models import BookModel


class BookRepositoryImp(BookRepository):
    def find_by_isbn(self, session, isbn: ISBN) -> Book | None:
        query = select(
            BookModel.isbn,
            BookModel.title,
            BookModel.author,
            BookModel.is_available,
        ).where(BookModel.isbn == isbn.value)

        row = session.execute(query).one_or_none()

        return (
            Book(
                isbn=ISBN(row.isbn),
                title=row.title,
                author=row.author,
                is_available=row.is_available,
            )
            if row
            else None
        )

    def save(self, session, book: Book) -> None:
        model = BookModel(
            isbn=book.isbn.value,
            title=book.title,
            author=book.author,
            is_available=book.is_available,
        )

        # 없으면 insert, 있으면 update
        session.merge(model)
