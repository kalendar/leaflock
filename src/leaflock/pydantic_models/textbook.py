import uuid

from pydantic import BaseModel

from .activity import Activity
from .module import Module


class Textbook(BaseModel):
    guid: uuid.UUID
    title: str
    prompt: str
    authors: str

    activities: set[Activity]
    modules: set[Module]

    def __hash__(self) -> int:
        return hash(self.guid)
