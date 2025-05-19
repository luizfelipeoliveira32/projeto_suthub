from fastapi import APIRouter, HTTPException, status
from database import age_groups_collection, enrollments_collection
from models.enrollment_request import EnrollmentRequest 
from models.enrollment_status import EnrollmentStatus

router = APIRouter()

@router.post("/enroll", status_code=status.HTTP_201_CREATED)
async def enroll_user(data: EnrollmentRequest):
    # Verificar se já existe matrícula para esse CPF
    existing = await enrollments_collection.find_one({"cpf": data.cpf})
    if existing:
        raise HTTPException(status_code=400, detail="Enrollment already exists")

    # Verificar se a idade está em alguma faixa cadastrada
    found_group = await age_groups_collection.find_one({
        "min_age": {"$lte": data.age},
        "max_age": {"$gte": data.age}
    })

    if not found_group:
        raise HTTPException(status_code=400, detail="Age not allowed for enrollment")

    # Inserir matrícula com status 'pending'
    enrollment = data.dict()
    enrollment["status"] = "pending"
    await enrollments_collection.insert_one(enrollment)

    return {"message": "Enrollment submitted", "status": "pending"}

@router.get("/enroll/{cpf}", response_model=EnrollmentStatus)
async def get_enrollment_status(cpf: str):
    enrollment = await enrollments_collection.find_one({"cpf": cpf})
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    return EnrollmentStatus(cpf=enrollment["cpf"], status=enrollment["status"])
