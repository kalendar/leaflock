from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel
from sqlalchemy import Dialect, MetaData, String, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase


class AttributeType(TypeDecorator[dict[str, Any] | BaseModel]):
    impl = String

    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect):
        if dialect.name == "sqlite":
            return dialect.type_descriptor(String())
        elif dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())

        return dialect.type_descriptor(String())

    def process_bind_param(
        self,
        value: dict[str, Any] | BaseModel | None,
        dialect: Dialect,
    ):
        if value is None:
            return None

        if dialect.name == "postgresql":
            if isinstance(value, BaseModel):
                return value.model_dump()
            else:
                return value

        if isinstance(value, BaseModel):
            return value.model_dump_json()
        else:
            return json.dumps(value)

    def process_result_value(
        self,
        value: dict[str, Any] | str | None,
        dialect: Dialect,
    ) -> dict[str, Any] | BaseModel | None:
        if value is None:
            return None

        if isinstance(value, dict):
            return value  # PostgreSQL returns a dictionary natively

        try:
            data = json.loads(value)  # SQLite stores JSON as a string
        except json.JSONDecodeError:
            return None  # If decoding fails, return None (or handle as needed)

        if isinstance(data, dict):
            return data  # type: ignore # Ensure the output type matches expectations

        return None  # Fallback to ensure type safety


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    type_annotation_map = {  # type: ignore
        dict[str, Any]: AttributeType,
        BaseModel: AttributeType,
    }
