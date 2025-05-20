from bson import ObjectId
from database import age_groups_collection, enrollments_collection
from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from models.age_group_in_out import AgeGroupIn, AgeGroupOut 
from models.enrollment_request import EnrollmentRequest
from models.enrollment_status import EnrollmentStatus
from routes import age_groups, enrollments

app = FastAPI(title="API for SUTHUB's case")

@app.get("/")
def read_root():
    return {"message": "FastAPI + MongoDB funcionando!"}


#app.include_router(age_groups.router)
#app.include_router(enrollments.router)

app.include_router(age_groups.router, prefix="/age-groups", tags=["Age Groups"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])

# Customização do esquema OpenAPI para habilitar o Basic Auth no Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SUTHUB case test",
        version="1.0.0",
        description="API protegida com autenticação HTTP Basic",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "basicAuth": {
            "type": "http",
            "scheme": "basic"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"basicAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi