from typing import Annotated
from fastapi import Depends,Request
from sqlalchemy.orm import Session
from database import SessionLocal
from core.security import verify_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict ,Depends(verify_token)]


def get_current_user_optinal(request:Request):
    try:
        return verify_token(request)
    except:
        return None