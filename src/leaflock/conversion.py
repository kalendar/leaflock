import uuid

from .pydantic_models import Activity as PydanticActivity
from .pydantic_models import Module as PydanticModule
from .pydantic_models import Textbook as PydanticTextbook
from .sqlalchemy_tables import Activity as SQLActivity
from .sqlalchemy_tables import Module as SQLModule
from .sqlalchemy_tables import Textbook as SQLTextbook


def sqla_to_pydantic(sqla_textbook: SQLTextbook) -> PydanticTextbook:
    return PydanticTextbook(
        guid=sqla_textbook.guid,
        title=sqla_textbook.title,
        prompt=sqla_textbook.prompt,
        authors=sqla_textbook.authors,
        activities=set(
            [
                PydanticActivity(
                    guid=activity.guid,
                    name=activity.name,
                    description=activity.description,
                    prompt=activity.prompt,
                    modules=set([module.guid for module in activity.modules]),
                )
                for activity in sqla_textbook.activities
            ]
        ),
        modules=set(
            [PydanticModule.model_validate(module) for module in sqla_textbook.modules]
        ),
    )


def pydantic_to_sqla(pydantic_textbook: PydanticTextbook) -> SQLTextbook:
    modules: set[SQLModule] = set()
    for pydantic_module in pydantic_textbook.modules:
        sql_module = SQLModule(
            name=pydantic_module.name,
            outcomes=pydantic_module.outcomes,
            summary=pydantic_module.summary,
        )
        sql_module.guid = pydantic_module.guid
        modules.add(sql_module)

    modules_by_guid: dict[uuid.UUID, SQLModule] = {
        module.guid: module for module in modules
    }

    activities: set[SQLActivity] = set()
    for pydantic_activity in pydantic_textbook.activities:
        sql_activity = SQLActivity(
            name=pydantic_activity.name,
            description=pydantic_activity.description,
            prompt=pydantic_activity.prompt,
        )

        for guid in pydantic_activity.modules:
            module = modules_by_guid.get(guid)
            if module is None:
                raise ValueError(f"No SQLModule with guid: {guid}")
            sql_activity.modules.add(module)

        sql_activity.guid = pydantic_activity.guid
        activities.add(sql_activity)

    return SQLTextbook(
        title=pydantic_textbook.title,
        prompt=pydantic_textbook.prompt,
        authors=pydantic_textbook.authors,
        activities=activities,
        modules=modules,
    )
