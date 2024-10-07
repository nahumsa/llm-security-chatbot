from pydantic import BaseModel


class ResponseModel(BaseModel):
    answer: str
    example_vulnerability: str
    example_attack: str
    prevention: str
