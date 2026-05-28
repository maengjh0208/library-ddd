from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from application.member_use_case import MemberUseCase
from infrastructure.database import get_session
from infrastructure.member_repository import MemberRepositoryImp

router = APIRouter(prefix="/members", tags=["members"])


class MemberRequest(BaseModel):
    member_id: str
    name: str


def get_member_use_case():
    return MemberUseCase(member_repository=MemberRepositoryImp())


# POST /members - 회원 등록
@router.post("")
def create_member(
    member_request: MemberRequest,
    session=Depends(get_session),
    use_case=Depends(get_member_use_case),
):
    try:
        member = use_case.create_member(
            session=session,
            member_id=member_request.member_id,
            name=member_request.name,
        )

        return {"member": member}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# GET /members/{member-id} - 회원 조회
@router.get("/{member_id}")
def get_member(
    member_id: str, session=Depends(get_session), use_case=Depends(get_member_use_case)
):
    try:
        member = use_case.get_member(
            session=session,
            member_id=member_id,
        )

        return {"member": member}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
