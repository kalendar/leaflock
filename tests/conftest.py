import uuid

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload, sessionmaker

from leaflock.pydantic_models import Activity as PydanticActivity
from leaflock.pydantic_models import Module as PydanticModule
from leaflock.pydantic_models import Textbook as PydanticTextbook
from leaflock.sqlalchemy_tables import Activity as SQLActivity
from leaflock.sqlalchemy_tables import Module as SQLModule
from leaflock.sqlalchemy_tables import Textbook as SQLTextbook
from src.leaflock.sqlalchemy_tables import Base


@pytest.fixture
def in_memory_database_session() -> sessionmaker[Session]:
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal


@pytest.fixture
def complete_textbook_model() -> PydanticTextbook:
    module_1_guid = uuid.uuid4()
    module_2_guid = uuid.uuid4()

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
                    modules=set([module_1_guid]),
                ),
                PydanticActivity(
                    guid=uuid.uuid4(),
                    name="Activity 2",
                    description="Activity description 2",
                    prompt="Activity prompt 2",
                    modules=set([module_1_guid, module_2_guid]),
                ),
            ]
        ),
        modules=set(
            [
                PydanticModule(
                    guid=module_1_guid,
                    name="Module 1",
                    outcomes="Module outcome 1",
                    summary="Module summary 1",
                ),
                PydanticModule(
                    guid=module_2_guid,
                    name="Module 2",
                    outcomes="Module outcome 2",
                    summary="Module summary 2",
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
        activities=set(
            [
                SQLActivity(
                    name=activity.name,
                    description=activity.description,
                    prompt=activity.prompt,
                )
                for activity in complete_textbook_model.activities
            ]
        ),
        modules=set(
            [
                SQLModule(
                    name=module.name,
                    outcomes=module.outcomes,
                    summary=module.summary,
                )
                for module in complete_textbook_model.modules
            ]
        ),
    )

    with in_memory_database_session.begin() as session:
        session.add(textbook_obj)

    with in_memory_database_session.begin() as session:
        expunged_textbook_obj = session.scalar(
            select(SQLTextbook).options(
                joinedload(SQLTextbook.activities).joinedload(SQLActivity.modules),
                joinedload(SQLTextbook.modules),
            )
        )
        if expunged_textbook_obj is None:
            raise ValueError("No textbook object!")

        session.expunge(expunged_textbook_obj)

    return expunged_textbook_obj
