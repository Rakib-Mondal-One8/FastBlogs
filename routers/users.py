from fastapi import APIRouter,status,HTTPException
from core.dependencies import db_dependency,user_dependency
from services import user_services
from schemas import PasswordChange,PhoneNumberChange,EmailUpdate

router = APIRouter(
    prefix='/api/v1/users/me',
    tags=['Users']
)

 
@router.get("",status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    return user_services.get_user(user,db)


@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,password_change:PasswordChange):
    return user_services.change_password(user,db,password_change)


@router.put("/phone",status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user:user_dependency,db:db_dependency,phone_number_change:PhoneNumberChange):
    print(phone_number_change.new_phone_number)
    return user_services.update_phone_number(user,db,phone_number_change)


@router.put("/email",status_code=status.HTTP_204_NO_CONTENT)
async def update_email(user:user_dependency,db:db_dependency,email_update:EmailUpdate):
    return user_services.update_email(user,db,email_update)