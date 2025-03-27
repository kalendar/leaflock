import uuid

from pydantic import BaseModel

from .activity import Activity
from .topic import Topic


class Textbook(BaseModel):
    guid: uuid.UUID

    title: str

    prompt: str

    authors: str
    reviewers: str

    activities: set[Activity]
    topics: set[Topic]

    def __hash__(self) -> int:
        return hash(self.guid)
