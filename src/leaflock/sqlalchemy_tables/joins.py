from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table, Uuid

from .base import Base

topic_activity = Table(
    "topic_activity",
    Base.metadata,
    Column("topic_id", Uuid, ForeignKey("topics.guid"), primary_key=True),  # type: ignore
    Column("activity_id", Uuid, ForeignKey("activities.guid"), primary_key=True),  # type: ignore
)
