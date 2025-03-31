import uuid

from pydantic import BaseModel


class Topic(BaseModel, from_attributes=True):
    guid: uuid.UUID

    name: str

    outcomes: str
    summary: str

    sources: str | None
    authors: str | None

    def __hash__(self) -> int:
        return hash(self.guid)
