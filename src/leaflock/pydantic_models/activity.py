import uuid

from pydantic import BaseModel, Field

from leaflock.licenses import License


class Activity(BaseModel, from_attributes=True):
    guid: uuid.UUID

    name: str

    prompt: str
    description: str | None

    sources: str | None
    authors: str | None

    license: License

    topics: set[uuid.UUID] = Field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.guid)
