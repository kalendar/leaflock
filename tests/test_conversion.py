import uuid

from leaflock.conversion import pydantic_to_sqla, sqla_to_pydantic
from leaflock.pydantic_models import Activity as PydanticActivity
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.pydantic_models import Topic as PydanticTopic
from leaflock.sqlalchemy_tables import Activity as SQLActivity
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook
from leaflock.sqlalchemy_tables import Topic as SQLTopic


def test_sqla_to_pydantic(complete_textbook_object: SQLTextbook):
    pydantic_textbook = sqla_to_pydantic(sqla_textbook=complete_textbook_object)

    # Assert that all textbook attributes are present and exact
    assert pydantic_textbook.title == complete_textbook_object.title
    assert pydantic_textbook.prompt == complete_textbook_object.prompt
    assert pydantic_textbook.authors == complete_textbook_object.authors

    sql_activity_by_guid: dict[uuid.UUID, SQLActivity] = {
        activity.guid: activity for activity in complete_textbook_object.activities
    }
    sql_topic_by_guid: dict[uuid.UUID, SQLTopic] = {
        topic.guid: topic for topic in complete_textbook_object.topics
    }

    # Assert that textbook activities and topics counts are correct
    assert len(pydantic_textbook.activities) == len(complete_textbook_object.activities)
    assert len(pydantic_textbook.topics) == len(complete_textbook_object.topics)

    # Assert that each activities' attributes are exactly the same
    for pydantic_activity in pydantic_textbook.activities:
        sql_activity = sql_activity_by_guid.get(pydantic_activity.guid)
        assert sql_activity is not None
        assert pydantic_activity.name == sql_activity.name
        assert pydantic_activity.description == sql_activity.description
        assert pydantic_activity.prompt == sql_activity.prompt
        assert len(pydantic_activity.topics) == len(sql_activity.topics)
        assert pydantic_activity.topics == sql_activity.topics

    # Assert that each topics' attributes are exactly the same
    for pydantic_topic in pydantic_textbook.topics:
        sql_topic = sql_topic_by_guid.get(pydantic_topic.guid)
        assert sql_topic is not None
        assert pydantic_topic.name == sql_topic.name
        assert pydantic_topic.summary == sql_topic.summary
        assert pydantic_topic.outcomes == sql_topic.outcomes


def test_pydantic_to_sqla(complete_textbook_model: PydanticTextbook):
    sql_textbook = pydantic_to_sqla(pydantic_textbook=complete_textbook_model)

    # Assert that all textbook attributes are present and exact
    assert sql_textbook.title == complete_textbook_model.title
    assert sql_textbook.prompt == complete_textbook_model.prompt
    assert sql_textbook.authors == complete_textbook_model.authors

    pydantic_activity_by_guid: dict[uuid.UUID, PydanticActivity] = {
        activity.guid: activity for activity in complete_textbook_model.activities
    }
    pydantic_topic_by_guid: dict[uuid.UUID, PydanticTopic] = {
        topic.guid: topic for topic in complete_textbook_model.topics
    }

    # Assert that textbook activities and topics counts are correct
    assert len(sql_textbook.activities) == len(complete_textbook_model.activities)
    assert len(sql_textbook.topics) == len(complete_textbook_model.topics)

    # Assert that each activities' attributes are exactly the same
    for sql_activity in complete_textbook_model.activities:
        pydantic_activity = pydantic_activity_by_guid.get(sql_activity.guid)
        assert pydantic_activity is not None
        assert sql_activity.name == pydantic_activity.name
        assert sql_activity.description == pydantic_activity.description
        assert sql_activity.prompt == pydantic_activity.prompt
        assert len(sql_activity.topics) == len(pydantic_activity.topics)
        assert sql_activity.topics == pydantic_activity.topics

    # Assert that each topics' attributes are exactly the same
    for sql_topic in complete_textbook_model.topics:
        pydantic_topics = pydantic_topic_by_guid.get(sql_topic.guid)
        assert pydantic_topics is not None
        assert sql_topic.name == pydantic_topics.name
        assert sql_topic.summary == pydantic_topics.summary
        assert sql_topic.outcomes == pydantic_topics.outcomes
