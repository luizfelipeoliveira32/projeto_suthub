from pydantic import BaseModel

class EnrollmentRequest(BaseModel):
    name: str
    age: int
    cpf: str