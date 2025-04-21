from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from leaflock.licenses import License

from .base import Base
from .joins import topic_activity
from .textbook import Textbook

if TYPE_CHECKING:
    from .topic import Topic


class Activity(MappedAsDataclass, Base):
    __tablename__ = "activities"

    guid: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        insert_default=uuid.uuid4,
    )

    name: Mapped[str]

    prompt: Mapped[str]

    license: Mapped[License]

    position: Mapped[int | None] = mapped_column(default=None)

    description: Mapped[str | None] = mapped_column(default=None)

    sources: Mapped[str | None] = mapped_column(default=None)
    authors: Mapped[str | None] = mapped_column(default=None)

    textbook_guid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("textbooks.guid"),
        init=False,
    )
    textbook: Mapped[Textbook] = relationship(
        back_populates="activities",
        init=False,
    )

    topics: Mapped[set[Topic]] = relationship(
        default_factory=set,
        back_populates="activities",
        secondary=topic_activity,
    )

    def __hash__(self) -> int:
        return hash(self.guid)
