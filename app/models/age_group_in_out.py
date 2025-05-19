from pydantic import BaseModel

class AgeGroupIn(BaseModel):
    min_age: int
    max_age: int

class AgeGroupOut(AgeGroupIn):
    id: str