from domain.book.book import Book
from domain.book.book_repository import BookRepository
from domain.book.isbn import ISBN


class BookUseCase:
    def __init__(
        self,
        book_repository: BookRepository,
    ):
        self.book_repository = book_repository

    def create_book(self, session, isbn: str, title: str, author: str) -> Book:
        book = Book(
            isbn=ISBN(isbn),
            title=title,
            author=author,
        )

        self.book_repository.save(session, book)
        return book

    def get_book(self, session, isbn: str) -> Book:
        book = self.book_repository.find_by_isbn(session, ISBN(isbn))

        if not book:
            raise ValueError(f"책을 찾을 수 없음 | isbn: {isbn}")

        return book
