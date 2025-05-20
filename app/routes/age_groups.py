from auth import authenticate
from bson import ObjectId
from database import age_groups_collection
from fastapi import APIRouter, Depends, HTTPException, status
from models.age_group_in_out import AgeGroupIn, AgeGroupOut

router = APIRouter()

# Criar faixa etária
@router.post("/age-groups", response_model=AgeGroupOut, status_code=status.HTTP_201_CREATED, 
             dependencies=[Depends(authenticate)])
async def create_age_group(data: AgeGroupIn):
    result = await age_groups_collection.insert_one(data.dict())
    return AgeGroupOut(id=str(result.inserted_id), **data.dict())

# Listar faixas etárias
@router.get("/age-groups", response_model=list[AgeGroupOut], dependencies=[Depends(authenticate)])
async def list_age_groups():
    age_groups = []
    async for group in age_groups_collection.find():
        age_groups.append(
            AgeGroupOut(
                id=str(group["_id"]),
                min_age=group["min_age"],
                max_age=group["max_age"]
            )
        )
    return age_groups

# Buscar faixa etária por ID
@router.get("/age-groups/{group_id}", response_model=AgeGroupOut, dependencies=[Depends(authenticate)])
async def get_age_group(group_id: str):
    group = await age_groups_collection.find_one({"_id": ObjectId(group_id)})
    if not group:
        raise HTTPException(status_code=404, detail="Age group not found")
    return AgeGroupOut(
        id=str(group["_id"]),
        min_age=group["min_age"],
        max_age=group["max_age"]
    )

# Atualizar faixa etária por ID
@router.put("/age-groups/{group_id}", response_model=AgeGroupOut, dependencies=[Depends(authenticate)])
async def update_age_group(group_id: str, data: AgeGroupIn):
    result = await age_groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$set": data.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Age group not found")
    return AgeGroupOut(id=group_id, **data.dict())

# Deletar faixa etária
@router.delete("/age-groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, 
               dependencies=[Depends(authenticate)])
async def delete_age_group(group_id: str):
    result = await age_groups_collection.delete_one({"_id": ObjectId(group_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Age group not found")
    return None