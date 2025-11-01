from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_current_user(db: Session = Depends(get_db)):
    """
    현재 사용자 정보 조회
    TODO: 구현 필요
    """
    return {"message": "사용자 정보 조회 API (구현 예정)"}

@router.put("/me/subscription-info")
def update_subscription_info(db: Session = Depends(get_db)):
    """
    사용자의 청약 정보 수정
    TODO: 구현 필요
    """
    return {"message": "청약 정보 수정 API (구현 예정)"}

@router.get("/me/preferences")
def get_preferences(db: Session = Depends(get_db)):
    """
    사용자의 희망 조건 조회
    TODO: 구현 필요
    """
    return {"message": "희망 조건 조회 API (구현 예정)"}

@router.put("/me/preferences")
def update_preferences(db: Session = Depends(get_db)):
    """
    사용자의 희망 조건 수정
    TODO: 구현 필요
    """
    return {"message": "희망 조건 수정 API (구현 예정)"}

@router.put("/me/auto-apply-mode")
def update_auto_apply_mode(db: Session = Depends(get_db)):
    """
    자동 신청 모드 변경
    TODO: 구현 필요
    """
    return {"message": "자동 신청 모드 변경 API (구현 예정)"}

@router.put("/me/notification-settings")
def update_notification_settings(db: Session = Depends(get_db)):
    """
    알림 수신 설정 변경
    TODO: 구현 필요
    """
    return {"message": "알림 설정 변경 API (구현 예정)"}

