# BookRepository 인터페이스


from abc import ABC, abstractmethod

from domain.book import Book
from domain.isbn import ISBN


# 추상 클래스
class BookRepository(ABC):
    @abstractmethod
    def find_by_isbn(self, session, isbn: ISBN) -> Book | None:
        pass

    @abstractmethod
    def save(self, session, book: Book) -> None:
        # isbn: ISBN, title: str, author: str 이런식으로 필드를 하나씩 받기보다는,
        # 이미 만들어진 객체(Book)를 받는게 더 자연스럽다.

        # post_book 과 같은 함수명보다는 save 함수명이 더 낫다.
        # post는 http 메서드 느낌이 나고,
        # Repository는 DB/HTTP를 모르는 domain개념이라 이름을 다르게 짓는게 좋다.

        pass
