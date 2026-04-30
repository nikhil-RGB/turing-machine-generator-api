from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import get_db
from models import Machines
from routers.auth import get_current_user
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status

router=APIRouter(prefix='/machines', tags=['machines'])


db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

# For body structure and syntax validation
class MachineRequest(BaseModel):
    
    name:str=Field(min_length=1,max_length=20)
    machine_data:str=Field(min_length=1)
    group_name:str= Field(min_length=1,max_length=20)
    
# Returns all machines as per who is owner, using owner_id
@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    return db.query(Machines).filter(Machines.owner_id==user.get('id')).all()
    
# Returns a particular machine, as identified by its id
# Note: The current user must own the machine for it to be displayed
@router.get("/{machine_id}",status_code=status.HTTP_200_OK)
async def read_by_id(user:user_dependency,db:db_dependency,machine_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    machine_model=db.query(Machines).filter(Machines.owner_id==user.get('id')).filter(Machines.id==machine_id).first()
    if machine_model is not None:
        return machine_model
    raise HTTPException(status_code=404,detail="Machine not found")

# Create a new machine
@router.post("/create_machine",status_code=status.HTTP_201_CREATED)
async def create_machine(user:user_dependency,db:db_dependency,machine_req:MachineRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    machine_model=Machines(**machine_req.model_dump(),owner_id=user.get('id'))
    db.add(machine_model)
    db.commit()
    # Finalize and commit creation operation

# Edit a Machine referencing it's machine id
@router.put("/update_machine/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_machine(user:user_dependency,db:db_dependency,machine_req:MachineRequest,id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    machine_model=db.query(Machines).filter(Machines.owner_id==user.get('id')).filter(Machines.id==id).first()
    if machine_model is None:
        raise HTTPException(status_code=404,detail="Machine not found")
    machine_model.group_name=machine_req.group_name
    machine_model.name=machine_req.name
    machine_model.machine_data=machine_req.machine_data
    db.add(machine_model)
    db.commit()
    #Finalize and commit update operation

# Delete a Machine referencing it's machine id
@router.delete("/delete_machine/{machine_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_machine(user:user_dependency,db:db_dependency,machine_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    machine_model=db.query(Machines).filter(Machines.owner_id==user.get('id')).filter(Machines.id==machine_id).first()
    if machine_model is None:
        raise HTTPException(status_code=404,detail="Machine not found")
    db.delete(machine_model)
    db.commit()
    #Finalize and commit delete operation
