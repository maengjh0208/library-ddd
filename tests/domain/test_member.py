from domain.member.member import Member


def test_member_create():
    member_id = "member_001"
    name = "juhee"

    member = Member(
        member_id=member_id,
        name=name,
    )

    assert member.member_id == member_id
    assert member.name == name


def test_member_can_borrow():
    member_id = "member_001"
    name = "juhee"

    member = Member(
        member_id=member_id,
        name=name,
    )

    assert member.can_borrow()


def test_member_cannot_borrow_when_count_is_3():
    # 대출 권수가 3권 이상이면 대출 불가
    member_id = "member_001"
    name = "juhee"
    loan_count = 3

    member = Member(
        member_id=member_id,
        name=name,
        loan_count=loan_count,
    )

    assert not member.can_borrow()


def test_member_cannot_borrow_when_overdue():
    # 연체가 있으면 대출 불가
    member_id = "member_001"
    name = "juhee"
    is_overdue = True

    member = Member(
        member_id=member_id,
        name=name,
        is_overdue=is_overdue,
    )

    assert not member.can_borrow()


def test_member_with_same_member_id_are_equal():
    # member_id 가 동일하면 동일한 객체
    member_id_1 = "member_001"
    name_1 = "juhee"

    member_1 = Member(
        member_id=member_id_1,
        name=name_1,
    )

    member_id_2 = "member_001"
    name_2 = "juhee2"

    member_2 = Member(
        member_id=member_id_2,
        name=name_2,
    )

    assert member_1 == member_2
