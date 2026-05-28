from dataclasses import dataclass


# frozen=True : 한번 객체 생성 후 값을 바꿀 수 없음 (바꾸면 에러)
@dataclass(frozen=True)
class ISBN:
    value: str

    # 잘못된 ISBN으로 객체가 만들어지면 안되므로 유효성 검사 필요
    def __post_init__(self):
        # dataclass는 __init__ 대신 여기서 유효성 검사를 한다.
        # frozen=True 여도 이 안에서는 초기화 가능

        # 하이픈 제거 후 숫자로만 되어 있고 13 자리인가?
        temp_value = self.value.replace("-", "")
        if not temp_value.isnumeric() or not len(temp_value) == 13:
            raise ValueError(f"유효하지 않은 ISBN: {self.value}")
