from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from .base import Base
from .joins import module_activity
from .textbook import Textbook

if TYPE_CHECKING:
    from .module import Module


class Activity(MappedAsDataclass, Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    name: Mapped[str]
    outcomes: Mapped[str]
    summary: Mapped[str]

    textbook_id: Mapped[int] = mapped_column(ForeignKey("textbooks.id"))
    textbook: Mapped[Textbook] = relationship(back_populates="activities", init=False)

    modules: Mapped[set[Module]] = relationship(
        default_factory=set,
        back_populates="activities",
        secondary=module_activity,
    )

    def __hash__(self) -> int:
        return hash(f"{self.id}{self.name}{self.textbook_id}")
