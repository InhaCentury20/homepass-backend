from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("")
def get_notifications(db: Session = Depends(get_db)):
    """
    알림 목록 조회
    TODO: 구현 필요
    """
    return {"message": "알림 목록 조회 API (구현 예정)"}

@router.post("/read")
def mark_notification_as_read(db: Session = Depends(get_db)):
    """
    알림 읽음 처리
    TODO: 구현 필요
    """
    return {"message": "알림 읽음 처리 API (구현 예정)"}

