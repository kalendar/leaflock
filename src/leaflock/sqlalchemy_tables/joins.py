from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table

from .base import Base

topic_activity = Table(
    "topic_activity",
    Base.metadata,
    Column("topic_id", String, ForeignKey("topics.guid"), primary_key=True),
    Column("activity_id", String, ForeignKey("activities.guid"), primary_key=True),
)
