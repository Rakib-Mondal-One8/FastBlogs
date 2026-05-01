from datetime import datetime, timezone
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt,JWTError



pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"


def create_access_token(user, expires_on):
    encode = {"sub": user.username, "user_id": user.id, "role": user.role}
    expires = datetime.now(timezone.utc) + expires_on
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("user_id")
        role = payload.get("role")
        
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a valid user!"
            )
        
        return {"username":username,'user_id':user_id,'role':role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a valid user!"
        )
