from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base

module_activity = Table(
    "module_activity",
    Base.metadata,
    Column("module_id", Integer, ForeignKey("modules.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)
