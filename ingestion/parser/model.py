from pydantic import BaseModel


class Section(BaseModel):
    name: str
    content: str


class File(BaseModel):
    name: str
    sections: list[Section]
