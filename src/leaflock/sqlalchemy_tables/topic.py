from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from .base import Base
from .joins import topic_activity
from .textbook import Textbook

if TYPE_CHECKING:
    from .activity import Activity
    from .textbook import Textbook


class Topic(MappedAsDataclass, Base):
    __tablename__ = "topics"

    guid: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        insert_default=uuid.uuid4,
    )

    name: Mapped[str]

    outcomes: Mapped[str]
    summary: Mapped[str]

    sources: Mapped[str | None] = mapped_column(default=None)
    authors: Mapped[str | None] = mapped_column(default=None)

    textbook_guid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("textbooks.guid"),
        init=False,
    )
    textbook: Mapped[Textbook] = relationship(
        back_populates="topics",
        init=False,
    )

    activities: Mapped[set[Activity]] = relationship(
        default_factory=set,
        back_populates="topics",
        secondary=topic_activity,
    )

    def __hash__(self) -> int:
        return hash(self.guid)
