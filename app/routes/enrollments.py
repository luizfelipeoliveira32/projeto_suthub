from app.auth import authenticate
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import age_groups_collection, enrollments_collection
from app.models.enrollment_request import EnrollmentRequest 
from app.models.enrollment_status import EnrollmentStatus

router = APIRouter()

@router.post("/enroll/{cpf}", response_model=EnrollmentStatus, status_code=status.HTTP_201_CREATED)
async def create_enrollment(data: EnrollmentRequest):
    age_groups = await age_groups_collection.find().to_list(None)

    idade_valida = any(group["min_age"] <= data.age <= group["max_age"] for group in age_groups)

    if not idade_valida:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Idade não corresponde a nenhum grupo de idade registrado."
        )

    enrollment_data = data.model_dump()
    enrollment_data["status"] = "pendente"

    await enrollments_collection.insert_one(enrollment_data)

    return EnrollmentStatus(cpf=data.cpf, status="pendente")

@router.get("/enroll/{cpf}", response_model=EnrollmentStatus, dependencies=[Depends(authenticate)])
async def get_enrollment_status(cpf: str):
    enrollment = await enrollments_collection.find_one({"cpf": cpf})
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    return EnrollmentStatus(cpf=enrollment["cpf"], status=enrollment["status"])
