from datetime import datetime, timedelta, timezone
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, Response,status,Request,Cookie
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import ExpiredSignatureError, jwt,JWTError
from models import Users
from services.cache_service import redis

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login',status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response

def create_access_token(user, expires_on):
    encode = {"sub": user.username, "user_id": user.id, "role": user.role}
    expires = datetime.now(timezone.utc) + expires_on
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user,expires_on):
    encode = {'sub':user.username,"user_id":user.id,"role":user.role,'type':'refresh'}
    expires = datetime.now(timezone.utc)+expires_on
    encode.update({'exp':expires})

    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


def _decode(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except ExpiredSignatureError:
        raise
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")


def _extract(payload: dict) -> dict:
    username, user_id, role = (
        payload.get("sub"),
        payload.get("user_id"),
        payload.get("role"),
    )
    if not username or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token claims.")
    return {"username": username, "user_id": user_id, "role": role}
    

async def verify_token(
    response: Response,
    access_token: str = Cookie(None),
    refresh_token: str = Cookie(None),
) -> dict:
    
    if access_token:
        try:
            return _extract(_decode(access_token))
        except ExpiredSignatureError:
            pass 


    if not refresh_token:
        raise HTTPException(status_code=401, detail="Not logged in.")

    try:
        payload = _decode(refresh_token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")


    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type.")

    user_data = _extract(payload)

    stored = await redis.get(f"refresh_token:{user_data['user_id']}")
    if not stored or stored != refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token revoked.")

    new_token = create_access_token(
        Users(id=user_data['user_id'],username=user_data['username'],role=user_data['role']),
        timedelta(seconds=5),
    )
    response.set_cookie(
        key="access_token",
        value=new_token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=5,
    )

    return user_data