from abc import ABC, abstractmethod

from domain.loan.loan import Loan


class LoanRepository(ABC):
    @abstractmethod
    def find_by_id(self, session, loan_id: str) -> Loan | None:
        pass

    @abstractmethod
    def save(self, session, loan: Loan) -> None:
        pass
