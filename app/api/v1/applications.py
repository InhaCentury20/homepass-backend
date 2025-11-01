from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("")
def get_applications(db: Session = Depends(get_db)):
    """
    나의 신청 내역 조회
    - 상태별 필터링 지원
    TODO: 구현 필요
    """
    return {"message": "신청 내역 조회 API (구현 예정)"}

@router.get("/{application_id}")
def get_application_detail(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    신청 내역 상세 조회
    TODO: 구현 필요
    """
    return {
        "message": "신청 내역 상세 조회 API (구현 예정)",
        "application_id": application_id
    }

@router.post("")
def create_application(db: Session = Depends(get_db)):
    """
    청약 자동 신청 요청
    - '알림 후 승인' 모드에서 사용
    TODO: 구현 필요
    """
    return {"message": "청약 신청 API (구현 예정)"}

