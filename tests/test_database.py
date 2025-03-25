import uuid
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from leaflock.database import create_database, upgrade_database
from leaflock.pydantic_models import Activity as PydanticActivity
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.pydantic_models import Topic as PydanticTopic
from leaflock.sqlalchemy_tables import Activity as SQLActivity
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook
from leaflock.sqlalchemy_tables import Topic as SQLTopic


@pytest.fixture
def textbook_data() -> PydanticTextbook:
    return PydanticTextbook(
        guid=uuid.uuid4(),
        title="Test Title",
        prompt="Test prompt.",
        authors="Author 1\nAuthor 2.",
        activities=set(
            [
                PydanticActivity(
                    guid=uuid.uuid4(),
                    name="Activity 1",
                    description="Activity description 1",
                    prompt="Activity prompt 1",
                ),
                PydanticActivity(
                    guid=uuid.uuid4(),
                    name="Activity 2",
                    description="Activity description 2",
                    prompt="Activity prompt 2",
                ),
            ]
        ),
        topics=set(
            [
                PydanticTopic(
                    guid=uuid.uuid4(),
                    name="Topic 1",
                    outcomes="Topic outcome 1",
                    summary="Topic summary 1",
                ),
                PydanticTopic(
                    guid=uuid.uuid4(),
                    name="Topic 2",
                    outcomes="Topic outcome 2",
                    summary="Topic summary 2",
                ),
            ]
        ),
    )


def test_create_database_in_memory(in_memory_database_session: sessionmaker[Session]):
    assert bool(in_memory_database_session.begin()) is True


def test_create_database_as_file(file_database_path: Path):
    create_database(database_path=file_database_path)

    assert file_database_path.exists() and file_database_path.is_file()


def test_commit_and_query_textbook(
    in_memory_database_session: sessionmaker[Session], textbook_data: PydanticTextbook
):
    activities: set[SQLActivity] = set()
    for pydantic_activity in textbook_data.activities:
        sql_activity = SQLActivity(
            name=pydantic_activity.name,
            description=pydantic_activity.description,
            prompt=pydantic_activity.prompt,
        )
        sql_activity.guid = pydantic_activity.guid
        activities.add(sql_activity)

    topics: set[SQLTopic] = set()
    for pydantic_topic in textbook_data.topics:
        sql_topic = SQLTopic(
            name=pydantic_topic.name,
            outcomes=pydantic_topic.outcomes,
            summary=pydantic_topic.summary,
        )
        sql_topic.guid = pydantic_topic.guid
        topics.add(sql_topic)

    sql_textbook = SQLTextbook(
        title=textbook_data.title,
        prompt=textbook_data.prompt,
        authors=textbook_data.authors,
        activities=activities,
        topics=topics,
    )

    with in_memory_database_session.begin() as session:
        session.add(sql_textbook)

    with in_memory_database_session.begin() as session:
        textbook_obj = session.scalar(select(SQLTextbook))

        # Assert that all textbook columns are present and exact
        assert textbook_obj is not None
        assert textbook_obj.title == textbook_data.title
        assert textbook_obj.prompt == textbook_data.prompt
        assert textbook_obj.authors == textbook_data.authors

        pydantic_activity_by_guid: dict[uuid.UUID, PydanticActivity] = {
            activity.guid: activity for activity in textbook_data.activities
        }
        pydantic_topic_by_guid: dict[uuid.UUID, PydanticTopic] = {
            topic.guid: topic for topic in textbook_data.topics
        }

        # Assert that textbook activities and topics counts are correct
        assert len(textbook_obj.activities) == len(textbook_data.activities)
        assert len(textbook_obj.topics) == len(textbook_data.topics)

        # Assert that each activities' attributes are exactly the same
        for activity in textbook_obj.activities:
            pydantic_activity = pydantic_activity_by_guid.get(activity.guid)
            assert pydantic_activity is not None
            assert activity.name == pydantic_activity.name
            assert activity.description == pydantic_activity.description
            assert activity.prompt == pydantic_activity.prompt

        # Assert that each topics' attributes are exactly the same
        for topic in textbook_obj.topics:
            pydantic_topic = pydantic_topic_by_guid.get(topic.guid)
            assert pydantic_topic is not None
            assert topic.name == pydantic_topic.name
            assert topic.summary == pydantic_topic.summary
            assert topic.outcomes == pydantic_topic.outcomes


def test_database_upgrade(file_database_path: Path):
    upgrade_database(database_path=file_database_path)

    assert file_database_path.exists() and file_database_path.is_file()

    engine = create_engine(f"sqlite:///{file_database_path}")

    # Table/column exists
    assert engine.connect().exec_driver_sql("SELECT version_num FROM alembic_version")
