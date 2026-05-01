from typing import Annotated
from fastapi import Depends
from pytest import Session
from database import SessionLocal
from core.security import verify_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict(),Depends(verify_token)]
