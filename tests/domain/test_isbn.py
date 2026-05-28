import pytest

from domain.book.isbn import ISBN


def test_isbn_success():
    # 테스트는 보통 3단계를 사용한다. - AAA 패턴

    # Arrange (준비) - 테스트에 필요한 값 세팅
    valid_isbn = "978-89-1234-567-8"

    # Act (실행) - 실제로 동작 실행
    isbn = ISBN(valid_isbn)

    # Assert (검증) - 결과가 기댓값과 같은지 확인
    assert isbn.value == valid_isbn


def test_isbn_fail_1():
    # isbn 실패 케이스 - 빈 문자열 테스트
    invalid_isbn = ""

    with pytest.raises(ValueError):
        ISBN(invalid_isbn)


def test_isbn_fail_2():
    # isbn 실패 케이스 - 형식 불일치
    invalid_isbn = "978-89-1234-567"

    with pytest.raises(ValueError):
        ISBN(invalid_isbn)
