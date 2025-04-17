from __future__ import annotations

import uuid
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from sqlalchemy.ext.orderinglist import ordering_list  # type: ignore
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .activity import Activity
    from .topic import Topic


class TextbookStatus(StrEnum):
    draft = "draft"
    published = "published"  # type: ignore


class Textbook(MappedAsDataclass, Base):
    __tablename__ = "textbooks"

    guid: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        insert_default=uuid.uuid4,
    )

    title: Mapped[str]
    prompt: Mapped[str]

    authors: Mapped[str | None] = mapped_column(default=None)
    reviewers: Mapped[str | None] = mapped_column(default=None)

    status: Mapped[TextbookStatus] = mapped_column(default=TextbookStatus.draft)

    edition: Mapped[str] = mapped_column(default="First Edition")
    schema_version: Mapped[str] = mapped_column(default="0.2.0")

    attributes: Mapped[dict[str, Any]] = mapped_column(default_factory=dict)

    activities: Mapped[list[Activity]] = relationship(
        default_factory=list,
        back_populates="textbook",
        order_by="Activity.position",
        collection_class=ordering_list("position"),  # type: ignore
        cascade="all, delete-orphan",
    )

    topics: Mapped[list[Topic]] = relationship(
        default_factory=list,
        back_populates="textbook",
        order_by="Topic.position",
        collection_class=ordering_list("position"),  # type: ignore
        cascade="all, delete-orphan",
    )

    def __hash__(self) -> int:
        return hash(self.guid)
