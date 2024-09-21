from typing import Annotated, Optional, Literal
from pydantic import BaseModel, Field


class ElasticDocument(BaseModel):
    title: str
    description: Annotated[str, Field(alias="Description")]
    example_vulnerabilities: Annotated[
        str, Field(alias="Common Examples of Vulnerability")
    ]
    mitigation: Annotated[str, Field(alias="Prevention and Mitigation Strategies")]
    example_attacks: Annotated[str, Field(alias="Example Attack Scenarios")]
    references: Annotated[Optional[str], Field(alias="Reference Links")] = None


class Property(BaseModel):
    type: Literal["keyword", "date"]


class Mappings(BaseModel):
    properties: dict[str, Property]


class Settings(BaseModel):
    number_of_shards: int
    number_of_replicas: int


class IndexSettings(BaseModel):
    settings: Settings
    mappings: Mappings
