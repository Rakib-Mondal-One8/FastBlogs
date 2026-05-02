from datetime import timedelta

import pytest
from .utils import *
from services.auth_services import authenticate_user,create_user
from fastapi import HTTPException
from core.security import create_access_token,verify_token


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_token] = override_verify_token


def test_create_access_token(test_user):

    token = create_access_token(test_user,timedelta(minutes=20))
    response = verify_token(token)
    assert response == {"username": test_user.username, "user_id": 1, "role": test_user.role}


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    response = authenticate_user(test_user.username,'rakib123',db)
    assert response.username == test_user.username


def test_create_user_existing(test_user):
    db = TestingSessionLocal()

    with pytest.raises(HTTPException) as exc:
        create_user(db,test_user)
    
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user():
    request_data = {
            'email':"rakib123@gmail.com",
            'username':"Rakib2340ne8",
            'first_name':"Rakib",
            'last_name':"Mondal",
            'role':"admin",
            'password':"rakib123",
            'phone_number':'9832760260',
    }
    response = client.post("/api/v1/auth/register",json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


def test_login(test_user):
    request_data = {
        'username':'Rakib0ne8',
        'password':'rakib123'
    }

    response = client.post("/api/v1/auth/token",data=request_data)
    assert response.json() == {"access_token":'token','token_type':'bearer'}


def test_login_invalid_password(test_user):
    request_data = {
        'username':'Rakib0ne8',
        'password':'rakib12'
    }
    response = client.post("/api/v1/auth/token",data=request_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
