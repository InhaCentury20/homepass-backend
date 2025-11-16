from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Announcement
from app.schemas import (
    AnnouncementDetailSchema,
    AnnouncementListResponse,
    AnnouncementSchema,
)

router = APIRouter(prefix="/announcements", tags=["announcements"])


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _calculate_dday(end_at: datetime | None) -> int | None:
    if not end_at:
        return None
    days = (end_at.date() - _now().date()).days
    return days if days >= 0 else None


def _serialize_announcement(announcement: Announcement) -> AnnouncementSchema:
    dday = _calculate_dday(announcement.application_end_date)
    return AnnouncementSchema(
        announcement_id=announcement.announcement_id,
        title=announcement.title,
        housing_type=announcement.housing_type,
        region=announcement.region,
        address_detail=announcement.address_detail,
        source_organization=announcement.source_organization,
        source_url=announcement.source_url,
        original_pdf_url=announcement.original_pdf_url,
        latitude=float(announcement.latitude) if announcement.latitude is not None else None,
        longitude=float(announcement.longitude) if announcement.longitude is not None else None,
        application_end_date=announcement.application_end_date,
        scraped_at=announcement.scraped_at,
        min_deposit=announcement.min_deposit,
        max_deposit=announcement.max_deposit,
        monthly_rent=announcement.monthly_rent,
        total_households=announcement.total_households,
        eligibility=announcement.eligibility,
        commute_base_address=announcement.commute_base_address,
        commute_time=announcement.commute_time,
        image_urls=announcement.image_urls,
        is_customized=announcement.is_customized,
        dday=dday,
    )


@router.get("", response_model=AnnouncementListResponse)
def get_announcements(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    region: str | None = Query(None, description="지역 필터 (부분 일치)"),
    housing_type: str | None = Query(None, description="주택 유형 필터 (부분 일치)"),
    db: Session = Depends(get_db),
) -> AnnouncementListResponse:
    stmt = select(Announcement).order_by(Announcement.application_end_date.asc())
    announcements: List[Announcement] = list(db.scalars(stmt))

    if region:
        region_lower = region.lower()
        announcements = [
            ann for ann in announcements if (ann.region or "").lower().find(region_lower) != -1
        ]

    if housing_type:
        housing_lower = housing_type.lower()
        announcements = [
            ann for ann in announcements if (ann.housing_type or "").lower().find(housing_lower) != -1
        ]

    total = len(announcements)
    start = (page - 1) * size
    end = start + size
    sliced = announcements[start:end]

    items = [_serialize_announcement(ann) for ann in sliced]
    return AnnouncementListResponse(total=total, page=page, size=size, items=items)


@router.get("/{announcement_id}", response_model=AnnouncementDetailSchema)
def get_announcement_detail(
    announcement_id: int,
    db: Session = Depends(get_db),
) -> AnnouncementDetailSchema:
    announcement = db.get(Announcement, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다.")

    base = _serialize_announcement(announcement).model_dump()
    base["schedules"] = announcement.schedules
    return AnnouncementDetailSchema(**base)
