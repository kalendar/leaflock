from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from .base import Base
from .joins import module_activity
from .textbook import Textbook

if TYPE_CHECKING:
    from .activity import Activity
    from .textbook import Textbook


class Module(MappedAsDataclass, Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guid: Mapped[uuid.UUID] = mapped_column(init=False, insert_default=uuid.uuid4)

    name: Mapped[str]
    outcomes: Mapped[str]
    summary: Mapped[str]

    textbook_id: Mapped[int] = mapped_column(ForeignKey("textbooks.id"), init=False)
    textbook: Mapped[Textbook] = relationship(back_populates="modules", init=False)

    activities: Mapped[set[Activity]] = relationship(
        default_factory=set,
        back_populates="modules",
        secondary=module_activity,
    )

    def __hash__(self) -> int:
        return hash(f"{self.id}{self.name}{self.textbook_id}")
