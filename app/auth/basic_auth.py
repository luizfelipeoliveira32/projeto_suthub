from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json
import secrets

security = HTTPBasic()

# Carrega credenciais estáticas do arquivo JSON
with open("credentials.json") as f:
    USERS = json.load(f)

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username in USERS
    correct_password = USERS.get(credentials.username) == credentials.password

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
