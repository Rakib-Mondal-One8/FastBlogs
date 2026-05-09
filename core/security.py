from datetime import datetime, timezone
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException,status,Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt,JWTError
from models import Users


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


def verify_token(request:Request):
    token = request.cookies.get('access_token')
    if(not token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not logged in.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("user_id")
        role = payload.get("role")
        
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a valid user."
            )
        return {"username":username,'user_id':user_id,'role':role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a valid user."
        )