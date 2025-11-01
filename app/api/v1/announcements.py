from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/announcements", tags=["announcements"])

@router.get("")
def get_announcements(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    region: str = Query(None),
    housing_type: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    공고 목록 조회
    - 필터링: region, housing_type
    - 페이징: page, size
    TODO: 구현 필요
    """
    return {
        "message": "공고 목록 조회 API (구현 예정)",
        "filters": {
            "page": page,
            "size": size,
            "region": region,
            "housing_type": housing_type
        }
    }

@router.get("/{announcement_id}")
def get_announcement_detail(
    announcement_id: int,
    db: Session = Depends(get_db)
):
    """
    공고 상세 정보 조회
    TODO: 구현 필요
    """
    return {
        "message": "공고 상세 정보 조회 API (구현 예정)",
        "announcement_id": announcement_id
    }

