from pydantic import BaseModel

class EnrollmentStatus(BaseModel):
    cpf: str
    status: str