from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException,Response
from schemas import UserCreate
from services import auth_services
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import db_dependency
from core.security import create_access_token
import os
IS_PRODUCTION = os.getenv("ENV") == "production"




router = APIRouter(
    prefix="/api/v1/auth",
    tags=['Auth']
)



@router.post("/register",status_code=status.HTTP_204_NO_CONTENT)
async def create_user(db:db_dependency,user_create:UserCreate):
    return auth_services.create_user(db,user_create)


@router.post("/token")
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency,response:Response):

    user = auth_services.authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not Valid!"
        )
    token = create_access_token(user,timedelta(minutes=20))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="strict" if IS_PRODUCTION else "lax",
        max_age=1200        # 20 minutes in seconds (matches your timedelta!)
    )

    return {"message":"Login Successful"}
