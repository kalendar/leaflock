import uuid

from pydantic import BaseModel


class Topic(BaseModel, from_attributes=True):
    guid: uuid.UUID
    name: str
    outcomes: str
    summary: str

    def __hash__(self) -> int:
        return hash(self.guid)
