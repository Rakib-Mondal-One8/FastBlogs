from datetime import datetime, timezone
from typing import Annotated
from core.security import pwd_context
from models import Users
from fastapi import HTTPException,status


def authenticate_user(username, password, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user  


def create_user(db,user_create):
    unique1 = db.query(Users).filter(Users.email == user_create.email).first()
    unique2 = db.query(Users).filter(Users.username == user_create.username).first()

    if unique1 is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered!")

    if unique2 is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered!"
        )

    user = Users(
        email=user_create.email,
        username=user_create.username,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        hashed_password=pwd_context.hash(user_create.password),
        phone_number=user_create.phone_number,
        role=user_create.role,
    )
    db.add(user)
    db.commit() 
    db.refresh(user) 
