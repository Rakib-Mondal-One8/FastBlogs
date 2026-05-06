from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends,HTTPException


from schemas import UserCreate
 
from services import auth_services
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import db_dependency
from core.security import create_access_token



router = APIRouter(
    prefix="/api/v1/auth",
    tags=['Auth']
)



@router.post("/register",status_code=status.HTTP_204_NO_CONTENT)
async def create_user(db:db_dependency,user_create:UserCreate):
    return auth_services.create_user(db,user_create)


@router.post("/token")
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):

    user = auth_services.authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not Valid!"
        )
    print(user)
    token = create_access_token(user,timedelta(minutes=20))

    return {"access_token" : token,"token_type":"bearer"}
