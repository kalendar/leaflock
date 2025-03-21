import uuid

from leaflock.conversion import pydantic_to_sqla, sqla_to_pydantic
from leaflock.pydantic_models import Activity as PydanticActivity
from leaflock.pydantic_models import Module as PydanticModule
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.sqlalchemy_tables import Activity as SQLActivity
from leaflock.sqlalchemy_tables import Module as SQLModule
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook


def test_sqla_to_pydantic(complete_textbook_object: SQLTextbook):
    pydantic_textbook = sqla_to_pydantic(sqla_textbook=complete_textbook_object)

    # Assert that all textbook attributes are present and exact
    assert pydantic_textbook.title == complete_textbook_object.title
    assert pydantic_textbook.prompt == complete_textbook_object.prompt
    assert pydantic_textbook.authors == complete_textbook_object.authors

    sql_activity_by_guid: dict[uuid.UUID, SQLActivity] = {
        activity.guid: activity for activity in complete_textbook_object.activities
    }
    sql_module_by_guid: dict[uuid.UUID, SQLModule] = {
        module.guid: module for module in complete_textbook_object.modules
    }

    # Assert that textbook activities and modules counts are correct
    assert len(pydantic_textbook.activities) == len(complete_textbook_object.activities)
    assert len(pydantic_textbook.modules) == len(complete_textbook_object.modules)

    # Assert that each activities' attributes are exactly the same
    for pydantic_activity in pydantic_textbook.activities:
        sql_activity = sql_activity_by_guid.get(pydantic_activity.guid)
        assert sql_activity is not None
        assert pydantic_activity.name == sql_activity.name
        assert pydantic_activity.description == sql_activity.description
        assert pydantic_activity.prompt == sql_activity.prompt
        assert len(pydantic_activity.modules) == len(sql_activity.modules)
        assert pydantic_activity.modules == sql_activity.modules

    # Assert that each modules' attributes are exactly the same
    for pydantic_module in pydantic_textbook.modules:
        sql_module = sql_module_by_guid.get(pydantic_module.guid)
        assert sql_module is not None
        assert pydantic_module.name == sql_module.name
        assert pydantic_module.summary == sql_module.summary
        assert pydantic_module.outcomes == sql_module.outcomes


def test_pydantic_to_sqla(complete_textbook_model: PydanticTextbook):
    sql_textbook = pydantic_to_sqla(pydantic_textbook=complete_textbook_model)

    # Assert that all textbook attributes are present and exact
    assert sql_textbook.title == complete_textbook_model.title
    assert sql_textbook.prompt == complete_textbook_model.prompt
    assert sql_textbook.authors == complete_textbook_model.authors

    pydantic_activity_by_guid: dict[uuid.UUID, PydanticActivity] = {
        activity.guid: activity for activity in complete_textbook_model.activities
    }
    pydantic_module_by_guid: dict[uuid.UUID, PydanticModule] = {
        module.guid: module for module in complete_textbook_model.modules
    }

    # Assert that textbook activities and modules counts are correct
    assert len(sql_textbook.activities) == len(complete_textbook_model.activities)
    assert len(sql_textbook.modules) == len(complete_textbook_model.modules)

    # Assert that each activities' attributes are exactly the same
    for sql_activity in complete_textbook_model.activities:
        pydantic_activity = pydantic_activity_by_guid.get(sql_activity.guid)
        assert pydantic_activity is not None
        assert sql_activity.name == pydantic_activity.name
        assert sql_activity.description == pydantic_activity.description
        assert sql_activity.prompt == pydantic_activity.prompt
        assert len(sql_activity.modules) == len(pydantic_activity.modules)
        assert sql_activity.modules == pydantic_activity.modules

    # Assert that each modules' attributes are exactly the same
    for sql_module in complete_textbook_model.modules:
        pydantic_module = pydantic_module_by_guid.get(sql_module.guid)
        assert pydantic_module is not None
        assert sql_module.name == pydantic_module.name
        assert sql_module.summary == pydantic_module.summary
        assert sql_module.outcomes == pydantic_module.outcomes
