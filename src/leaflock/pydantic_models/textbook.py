import uuid
from typing import Any

from pydantic import BaseModel, Field

from leaflock.sqlalchemy_tables.textbook import TextbookStatus

from .activity import Activity
from .topic import Topic


class Textbook(BaseModel):
    guid: uuid.UUID

    title: str
    prompt: str

    authors: str | None
    reviewers: str | None

    status: TextbookStatus = Field(default=TextbookStatus.draft)

    edition: str = Field(default="First Edition")
    schema_version: str = Field(default="0.2.0")

    attributes: dict[str, Any]

    activities: set[Activity]
    topics: set[Topic]

    def __hash__(self) -> int:
        return hash(self.guid)
