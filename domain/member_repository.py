# MemberRepository 인터페이스


from abc import ABC, abstractmethod

from domain.member import Member


# 추상 클래스
class MemberRepository(ABC):
    @abstractmethod
    def find_by_id(self, session, member_id: str) -> Member:
        pass

    @abstractmethod
    def save(self, session, member: Member) -> None:
        pass
