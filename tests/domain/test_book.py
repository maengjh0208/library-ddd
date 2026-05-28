from domain.book.book import Book
from domain.book.isbn import ISBN


def test_book_create():
    # 케이스: Book 정상 생성
    isbn = "978-89-1234-567-8"
    title = "책 제목"
    author = "책 저자"

    book = Book(
        isbn=ISBN(isbn),
        title=title,
        author=author,
    )

    assert book.isbn.value == isbn
    assert book.title == title
    assert book.author == author


def test_book_with_same_isbn_are_equal():
    # 테스트 함수 하나에 시나리오 하나가 원칙
    # 케이스: isbn 이 같으면 동등한 객체이다.
    isbn_1 = "978-89-1234-567-8"
    title_1 = "책 제목"
    author_1 = "책 저자"

    book_1 = Book(
        isbn=ISBN(isbn_1),
        title=title_1,
        author=author_1,
    )

    isbn_2 = "978-89-1234-567-8"
    title_2 = "책 다른제목"
    author_2 = "책 다른저자"

    book_2 = Book(
        isbn=ISBN(isbn_2),
        title=title_2,
        author=author_2,
    )

    assert book_1 == book_2
