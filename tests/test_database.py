import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from leaflock.pydantic_models import Activity as PydanticActivity
from leaflock.pydantic_models import Module as PydanticModule
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.sqlalchemy_tables import Activity as SQLActivity
from leaflock.sqlalchemy_tables import Module as SQLModule
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook


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
        modules=set(
            [
                PydanticModule(
                    guid=uuid.uuid4(),
                    name="Module 1",
                    outcomes="Module outcome 1",
                    summary="Module summary 1",
                ),
                PydanticModule(
                    guid=uuid.uuid4(),
                    name="Module 2",
                    outcomes="Module outcome 2",
                    summary="Module summary 2",
                ),
            ]
        ),
    )


def test_create_database(in_memory_database_session: sessionmaker[Session]):
    assert bool(in_memory_database_session.begin()) is True


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

    modules: set[SQLModule] = set()
    for pydantic_module in textbook_data.modules:
        sql_module = SQLModule(
            name=pydantic_module.name,
            outcomes=pydantic_module.outcomes,
            summary=pydantic_module.summary,
        )
        sql_module.guid = pydantic_module.guid
        modules.add(sql_module)

    sql_textbook = SQLTextbook(
        title=textbook_data.title,
        prompt=textbook_data.prompt,
        authors=textbook_data.authors,
        activities=activities,
        modules=modules,
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
        pydantic_module_by_guid: dict[uuid.UUID, PydanticModule] = {
            module.guid: module for module in textbook_data.modules
        }

        # Assert that textbook activities and modules counts are correct
        assert len(textbook_obj.activities) == len(textbook_data.activities)
        assert len(textbook_obj.modules) == len(textbook_data.modules)

        # Assert that each activities' attributes are exactly the same
        for activity in textbook_obj.activities:
            pydantic_activity = pydantic_activity_by_guid.get(activity.guid)
            assert pydantic_activity is not None
            assert activity.name == pydantic_activity.name
            assert activity.description == pydantic_activity.description
            assert activity.prompt == pydantic_activity.prompt

        # Assert that each modules' attributes are exactly the same
        for module in textbook_obj.modules:
            pydantic_module = pydantic_module_by_guid.get(module.guid)
            assert pydantic_module is not None
            assert module.name == pydantic_module.name
            assert module.summary == pydantic_module.summary
            assert module.outcomes == pydantic_module.outcomes
