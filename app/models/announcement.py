from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Announcement(Base):
    __tablename__ = "Announcements"

    announcement_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    source_organization = Column(String(100), nullable=True)
    source_url = Column(String(2048), nullable=True)
    housing_type = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    address_detail = Column(String(255), nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    application_end_date = Column(DateTime, nullable=True)
    parsed_content = Column(Text, nullable=True)
    original_pdf_url = Column(String(2048), nullable=True)
    scraped_at = Column(DateTime, nullable=True, server_default=func.current_timestamp())

    applications = relationship("Application", back_populates="announcement")
    notifications = relationship("Notification", back_populates="announcement")

    # Convenience helpers -------------------------------------------------
    def load_parsed_content(self) -> Dict[str, Any]:
        if not self.parsed_content:
            return {}
        try:
            return json.loads(self.parsed_content)
        except json.JSONDecodeError:
            return {}

    @property
    def image_urls(self) -> List[str]:
        data = self.load_parsed_content()
        images = data.get("image_urls", [])
        return images if isinstance(images, list) else []

    @property
    def min_deposit(self) -> Optional[int]:
        data = self.load_parsed_content()
        value = data.get("min_deposit")
        return int(value) if isinstance(value, (int, float)) else None

    @property
    def max_deposit(self) -> Optional[int]:
        data = self.load_parsed_content()
        value = data.get("max_deposit")
        return int(value) if isinstance(value, (int, float)) else None

    @property
    def monthly_rent(self) -> Optional[int]:
        data = self.load_parsed_content()
        value = data.get("monthly_rent")
        return int(value) if isinstance(value, (int, float)) else None

    @property
    def is_customized(self) -> bool:
        data = self.load_parsed_content()
        return bool(data.get("is_customized", False))

    @property
    def total_households(self) -> Optional[int]:
        data = self.load_parsed_content()
        value = data.get("total_households")
        return int(value) if isinstance(value, (int, float)) else None

    @property
    def eligibility(self) -> Optional[str]:
        data = self.load_parsed_content()
        value = data.get("eligibility")
        return str(value) if value else None

    @property
    def commute_base_address(self) -> Optional[str]:
        data = self.load_parsed_content()
        value = data.get("commute_base_address")
        return str(value) if value else None

    @property
    def commute_time(self) -> Optional[int]:
        data = self.load_parsed_content()
        value = data.get("commute_time")
        return int(value) if isinstance(value, (int, float)) else None

    @property
    def schedules(self) -> List[Dict[str, Any]]:
        data = self.load_parsed_content()
        schedules = data.get("schedules", [])
        return schedules if isinstance(schedules, list) else []

