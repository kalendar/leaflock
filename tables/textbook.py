from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .activity import Activity
    from .module import Module


class Textbook(MappedAsDataclass, Base):
    __tablename__ = "textbooks"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    title: Mapped[str]
    prompt: Mapped[str]
    authors: Mapped[str]

    activities: Mapped[set[Activity]] = relationship(
        default_factory=set,
        back_populates="textbook",
        cascade="all, delete",
    )

    modules: Mapped[set[Module]] = relationship(
        default_factory=set,
        back_populates="textbook",
        cascade="all, delete",
    )

    def __hash__(self) -> int:
        return hash(f"{self.id}{self.title}")
