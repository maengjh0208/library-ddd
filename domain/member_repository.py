# MemberRepository 인터페이스
# BookRepository 인터페이스


from abc import ABC, abstractmethod

from domain.member import Member


# 추상 클래스
class MemberRepository(ABC):
    @abstractmethod
    def find_by_id(self, member_id: str) -> Member:
        pass

    @abstractmethod
    def save(self, member: Member) -> None:
        pass
