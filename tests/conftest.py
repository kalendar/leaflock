import uuid
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload, sessionmaker

from leaflock.pydantic_models import Activity as PydanticActivity
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.pydantic_models import Topic as PydanticTopic
from leaflock.sqlalchemy_tables import Activity as SQLActivity
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook
from leaflock.sqlalchemy_tables import Topic as SQLTopic
from src.leaflock.sqlalchemy_tables import Base


@pytest.fixture
def in_memory_database_session() -> sessionmaker[Session]:
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal


@pytest.fixture
def file_database_path(tmp_path: Path) -> Path:
    database_path = tmp_path / "testing_database.db"
    return database_path


@pytest.fixture
def complete_textbook_model() -> PydanticTextbook:
    topic_1_guid = uuid.uuid4()
    topic_2_guid = uuid.uuid4()

    return PydanticTextbook(
        guid=uuid.uuid4(),
        title="Test Title",
        prompt="Test prompt.",
        authors="Author 1\nAuthor 2.",
        reviewers="Reviewer 1\nReviewer 2.",
        attributes={
            "attr_1": 1,
            "attr_2": "2",
        },
        activities=set(
            [
                PydanticActivity(
                    guid=uuid.uuid4(),
                    name="Activity 1",
                    description="Activity description 1",
                    prompt="Activity prompt 1",
                    topics=set([topic_1_guid]),
                    sources="Source 1",
                    authors="Author 1",
                ),
                PydanticActivity(
                    guid=uuid.uuid4(),
                    name="Activity 2",
                    description="Activity description 2",
                    prompt="Activity prompt 2",
                    topics=set([topic_1_guid, topic_2_guid]),
                    sources="Source 2",
                    authors="Author 2",
                ),
            ]
        ),
        topics=set(
            [
                PydanticTopic(
                    guid=topic_1_guid,
                    name="Topic 1",
                    outcomes="Topic outcome 1",
                    summary="Topic summary 1",
                    sources="Source 1",
                    authors="Author 1",
                ),
                PydanticTopic(
                    guid=topic_2_guid,
                    name="Topic 2",
                    outcomes="Topic outcome 2",
                    summary="Topic summary 2",
                    sources="Source 2",
                    authors="Author 2",
                ),
            ]
        ),
    )


@pytest.fixture
def complete_textbook_object(
    in_memory_database_session: sessionmaker[Session],
    complete_textbook_model: PydanticTextbook,
) -> SQLTextbook:
    textbook_obj = SQLTextbook(
        title=complete_textbook_model.title,
        prompt=complete_textbook_model.prompt,
        authors=complete_textbook_model.authors,
        reviewers=complete_textbook_model.reviewers,
        status=complete_textbook_model.status,
        attributes={
            "attr_1": 1,
            "attr_2": "2",
        },
        activities=set(
            [
                SQLActivity(
                    name=activity.name,
                    description=activity.description,
                    prompt=activity.prompt,
                    sources=activity.sources,
                    authors=activity.authors,
                )
                for activity in complete_textbook_model.activities
            ]
        ),
        topics=set(
            [
                SQLTopic(
                    name=topic.name,
                    outcomes=topic.outcomes,
                    summary=topic.summary,
                    sources=topic.sources,
                    authors=topic.authors,
                )
                for topic in complete_textbook_model.topics
            ]
        ),
    )

    with in_memory_database_session.begin() as session:
        session.add(textbook_obj)

    with in_memory_database_session.begin() as session:
        expunged_textbook_obj = session.scalar(
            select(SQLTextbook).options(
                joinedload(SQLTextbook.activities).joinedload(SQLActivity.topics),
                joinedload(SQLTextbook.topics),
            )
        )
        if expunged_textbook_obj is None:
            raise ValueError("No textbook object!")

        session.expunge(expunged_textbook_obj)

    return expunged_textbook_obj
