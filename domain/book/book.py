from dataclasses import dataclass

from domain.book.isbn import ISBN


@dataclass
class Book:
    isbn: ISBN  # ISBN
    title: str  # 책 제목
    author: str  # 저자
    is_available: bool = True  # 대출 가능 여부. 기본값 True (처음엔 대출 가능으로 설정)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return False

        return self.isbn == other.isbn

    # __eq__를 직접 정의하면 Python이 __hash__를 None으로 만들어버린다.
    def __hash__(self) -> int:
        return hash(self.isbn)
