from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class AttributeType(str, Enum):
    BOOLEAN = "crystal.topics.data.attribute-types.boolean"
    CATEGORICAL = "crystal.topics.data.attribute-types.categorical"
    DATETIME = "crystal.topics.data.attribute-types.datetime"
    NUMERIC = "crystal.topics.data.attribute-types.numeric"
    RELATIVE_TIME_RANGE = "crystal.topics.data.attribute-types.relative_timerange"
    STRUCT = "crystal.topics.data.attribute-types.scruct"
    ARRAY = "crystal.topics.data.attribute-types.array"
    UNKNOWN = "crystal.topics.data.attribute-types.unknown"


class Attribute(BaseModel):
    uid: str
    type: AttributeType  # noqa: A003
    filterable: bool
    sortable: bool


class AttributesSchema(BaseModel):
    attributes: List[Attribute] = Field(default=list())


class Collection(BaseModel):
    uid: str
    attributes_schema: AttributesSchema
