import uuid
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from leaflock.database import create_database, upgrade_database
from leaflock.licenses import License
from leaflock.pydantic_models import Activity as PydanticActivity
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.pydantic_models import Topic as PydanticTopic
from leaflock.sqlalchemy_tables import Activity as SQLActivity
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook
from leaflock.sqlalchemy_tables import Topic as SQLTopic


def test_create_database_in_memory(in_memory_database_session: sessionmaker[Session]):
    assert bool(in_memory_database_session.begin()) is True


def test_create_database_as_file(file_database_path: Path):
    create_database(database_path=file_database_path)

    assert file_database_path.exists() and file_database_path.is_file()


def test_commit_and_query_textbook(
    in_memory_database_session: sessionmaker[Session],
    complete_textbook_model: PydanticTextbook,
):
    activities: list[SQLActivity] = list()
    for pydantic_activity in complete_textbook_model.activities:
        sql_activity = SQLActivity(
            name=pydantic_activity.name,
            description=pydantic_activity.description,
            prompt=pydantic_activity.prompt,
            sources=pydantic_activity.sources,
            authors=pydantic_activity.authors,
            license=License.CC0_1_0,
        )
        sql_activity.guid = pydantic_activity.guid
        activities.append(sql_activity)

    topics: list[SQLTopic] = list()
    for pydantic_topic in complete_textbook_model.topics:
        sql_topic = SQLTopic(
            name=pydantic_topic.name,
            outcomes=pydantic_topic.outcomes,
            summary=pydantic_topic.summary,
            sources=pydantic_topic.sources,
            authors=pydantic_topic.authors,
            license=License.CC0_1_0,
        )
        sql_topic.guid = pydantic_topic.guid
        topics.append(sql_topic)

    sql_textbook = SQLTextbook(
        title=complete_textbook_model.title,
        prompt=complete_textbook_model.prompt,
        authors=complete_textbook_model.authors,
        reviewers=complete_textbook_model.reviewers,
        activities=activities,
        topics=topics,
    )

    # Add an activity to a topic.
    joined_topic = sql_textbook.topics.copy().pop()
    joined_activity = sql_textbook.activities.copy().pop()

    joined_topic.activities = set([joined_activity])

    joined_topic_guid = joined_topic.guid
    joined_activity_guid = joined_activity.guid

    with in_memory_database_session.begin() as session:
        session.add(sql_textbook)

    with in_memory_database_session.begin() as session:
        textbook_obj = session.scalar(select(SQLTextbook))

        # Assert that all textbook columns are present and exact
        assert textbook_obj is not None
        assert textbook_obj.title == complete_textbook_model.title
        assert textbook_obj.prompt == complete_textbook_model.prompt
        assert textbook_obj.authors == complete_textbook_model.authors

        pydantic_activity_by_guid: dict[uuid.UUID, PydanticActivity] = {
            activity.guid: activity for activity in complete_textbook_model.activities
        }
        pydantic_topic_by_guid: dict[uuid.UUID, PydanticTopic] = {
            topic.guid: topic for topic in complete_textbook_model.topics
        }

        # Assert that textbook activities and topics counts are correct
        assert len(textbook_obj.activities) == len(complete_textbook_model.activities)
        assert len(textbook_obj.topics) == len(complete_textbook_model.topics)

        # Assert that each activities' attributes are exactly the same
        for joined_activity in textbook_obj.activities:
            pydantic_activity = pydantic_activity_by_guid.get(joined_activity.guid)
            assert pydantic_activity is not None
            assert joined_activity.name == pydantic_activity.name
            assert joined_activity.description == pydantic_activity.description
            assert joined_activity.prompt == pydantic_activity.prompt

        # Assert that each topics' attributes are exactly the same
        for topic in textbook_obj.topics:
            pydantic_topic = pydantic_topic_by_guid.get(topic.guid)
            assert pydantic_topic is not None
            assert topic.name == pydantic_topic.name
            assert topic.summary == pydantic_topic.summary
            assert topic.outcomes == pydantic_topic.outcomes

        # Assert that a predefined topic has a predefined activity
        for topic in textbook_obj.topics:
            if topic.guid == joined_topic_guid:
                assert joined_activity_guid in [
                    activity.guid for activity in topic.activities
                ]


def test_database_upgrade(file_database_path: Path):
    upgrade_database(database_path=file_database_path)

    assert file_database_path.exists() and file_database_path.is_file()

    engine = create_engine(f"sqlite:///{file_database_path}")

    # Table/column exists
    assert engine.connect().exec_driver_sql("SELECT version_num FROM alembic_version")
