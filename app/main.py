from bson import ObjectId
from database import age_groups_collection, enrollments_collection
from fastapi import FastAPI, HTTPException, Depends
from models.age_group_in_out import AgeGroupIn, AgeGroupOut 
from models.enrollment_request import EnrollmentRequest
from models.enrollment_status import EnrollmentStatus
from routes import age_groups, enrollments

app = FastAPI(title="API for SUTHUB's case")

@app.get("/")
def read_root():
    return {"message": "FastAPI + MongoDB funcionando!"}

@app.post("/teste-input")
def teste(value: int):
    return {"message": value}

app.include_router(age_groups.router)
app.include_router(enrollments.router)
