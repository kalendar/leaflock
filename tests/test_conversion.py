from leaflock.conversion import pydantic_to_sqla, sqla_to_pydantic
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook


def test_sqla_to_pydantic(complete_textbook_object: SQLTextbook):
    pydantic_textbook = sqla_to_pydantic(sqla_textbook=complete_textbook_object)

    # Assert that all textbook attributes are present and exact
    assert pydantic_textbook.title == complete_textbook_object.title
    assert pydantic_textbook.prompt == complete_textbook_object.prompt
    assert pydantic_textbook.authors == complete_textbook_object.authors
    assert pydantic_textbook.reviewers == complete_textbook_object.reviewers
    assert pydantic_textbook.status == complete_textbook_object.status
    assert pydantic_textbook.edition == complete_textbook_object.edition
    assert pydantic_textbook.schema_version == complete_textbook_object.schema_version

    assert len(pydantic_textbook.attributes.keys()) == len(
        complete_textbook_object.attributes.keys()
    )

    for pydantic_key, sql_key in zip(
        pydantic_textbook.attributes.keys(), complete_textbook_object.attributes.keys()
    ):
        pydantic_value = pydantic_textbook.attributes.get(pydantic_key)
        sql_value = complete_textbook_object.attributes.get(sql_key)

        assert pydantic_value == sql_value

    # Assert that textbook activities and topics counts are correct
    assert len(pydantic_textbook.activities) == len(complete_textbook_object.activities)
    assert len(pydantic_textbook.topics) == len(complete_textbook_object.topics)

    # Assert that each activities' attributes are exactly the same, same order
    for sql_activity, pydantic_activity in zip(
        complete_textbook_object.activities,
        pydantic_textbook.activities,
    ):
        assert pydantic_activity.guid == sql_activity.guid
        assert pydantic_activity.name == sql_activity.name
        assert pydantic_activity.description == sql_activity.description
        assert pydantic_activity.prompt == sql_activity.prompt
        assert pydantic_activity.authors == sql_activity.authors
        assert pydantic_activity.sources == sql_activity.sources
        assert len(pydantic_activity.topics) == len(sql_activity.topics)
        assert pydantic_activity.topics == sql_activity.topics

    # Assert that each topics' attributes are exactly the same, same order
    for sql_topic, pydantic_topic in zip(
        complete_textbook_object.topics,
        pydantic_textbook.topics,
    ):
        assert pydantic_topic.guid == sql_topic.guid
        assert pydantic_topic.name == sql_topic.name
        assert pydantic_topic.summary == sql_topic.summary
        assert pydantic_topic.outcomes == sql_topic.outcomes
        assert pydantic_topic.authors == pydantic_topic.authors
        assert pydantic_topic.sources == pydantic_topic.sources


def test_pydantic_to_sqla(complete_textbook_model: PydanticTextbook):
    sql_textbook = pydantic_to_sqla(pydantic_textbook=complete_textbook_model)

    # Assert that all textbook attributes are present and exact
    assert sql_textbook.title == complete_textbook_model.title
    assert sql_textbook.prompt == complete_textbook_model.prompt
    assert sql_textbook.authors == complete_textbook_model.authors
    assert sql_textbook.reviewers == complete_textbook_model.reviewers
    assert sql_textbook.status == complete_textbook_model.status
    assert sql_textbook.edition == complete_textbook_model.edition
    assert sql_textbook.schema_version == complete_textbook_model.schema_version

    assert len(sql_textbook.attributes.keys()) == len(
        complete_textbook_model.attributes.keys()
    )

    for pydantic_key, sql_key in zip(
        complete_textbook_model.attributes.keys(), sql_textbook.attributes.keys()
    ):
        pydantic_value = complete_textbook_model.attributes.get(pydantic_key)
        sql_value = sql_textbook.attributes.get(sql_key)

        assert pydantic_value == sql_value

    # Assert that textbook activities and topics counts are correct
    assert len(sql_textbook.activities) == len(complete_textbook_model.activities)
    assert len(sql_textbook.topics) == len(complete_textbook_model.topics)

    # Assert that each activities' attributes are exactly the same, same order
    for sql_activity, pydantic_activity in zip(
        sql_textbook.activities,
        complete_textbook_model.activities,
    ):
        assert sql_activity.guid == pydantic_activity.guid
        assert sql_activity.name == pydantic_activity.name
        assert sql_activity.description == pydantic_activity.description
        assert sql_activity.prompt == pydantic_activity.prompt
        assert sql_activity.authors == pydantic_activity.authors
        assert sql_activity.sources == pydantic_activity.sources
        assert len(sql_activity.topics) == len(pydantic_activity.topics)
        assert (
            set([topic.guid for topic in sql_activity.topics])
            == pydantic_activity.topics
        )

    # Assert that each topics' attributes are exactly the same
    for sql_topic, pydantic_topic in zip(
        sql_textbook.topics,
        complete_textbook_model.topics,
    ):
        assert sql_topic.guid == pydantic_topic.guid
        assert sql_topic.name == pydantic_topic.name
        assert sql_topic.summary == pydantic_topic.summary
        assert sql_topic.outcomes == pydantic_topic.outcomes
        assert sql_topic.authors == pydantic_topic.authors
        assert sql_topic.sources == pydantic_topic.sources
