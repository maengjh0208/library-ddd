# conftest = configuration + test (테스트 설정 파일)
# pytest 실행 -> conftest.py 자동 로드 (fixture 등록) -> test_*.py 실행 (fixture 자동 주입)

import pytest

from domain.book.book import Book
from domain.book.isbn import ISBN
from domain.member.member import Member

# @pytest.fixture(scope="function")  # 기본값. 함수마다 새로 생성
# @pytest.fixture(scope="module")    # 파일 안에서 한 번만 생성
# @pytest.fixture(scope="session")   # 전체 테스트에서 한 번만 생성


@pytest.fixture
def book():
    return Book(
        isbn=ISBN("978-89-1234-567-8"),
        title="책 제목",
        author="책 저자",
    )


@pytest.fixture
def member():
    return Member(
        member_id="member_001",
        name="juhee",
    )
