from typing import Annotated
from fastapi import Depends,Request,Cookie,HTTPException, Response,status
from sqlalchemy.orm import Session
from database import SessionLocal
from core.security import verify_token
from jose import jwt,JWTError
from core.security import SECRET_KEY,ALGORITHM

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict ,Depends(verify_token)]


# ── Optional auth dependency (for public pages) ───────────────────────────────

async def get_current_user_optional(
    response: Response,
    access_token: str = Cookie(None),
    refresh_token: str = Cookie(None),
) -> dict | None:
    
    if not access_token and not refresh_token:
        return None
    try:
        return await verify_token(response, access_token, refresh_token)
    except HTTPException:
        return None