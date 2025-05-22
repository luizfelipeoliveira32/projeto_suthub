#from bson import ObjectId
#from database import age_groups_collection, enrollments_collection
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#from models.age_group_in_out import AgeGroupIn, AgeGroupOut 
#from models.enrollment_request import EnrollmentRequest
#from models.enrollment_status import EnrollmentStatus
from app.routes import age_groups, enrollments

app = FastAPI(title="API for SUTHUB's case")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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