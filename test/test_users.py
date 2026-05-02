from .utils import *


def test_get_user(test_user):
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'Rakib0ne8'


# def test_get_user_invalid(test_user):
#     response = client.get("/api/v1/users/me")
#     assert response.status_code == status.HTTP_200_OK
#     assert response == None

def test_change_password(test_user):
    request_body = {
        'password':'rakib123',
        'new_password':'rakib12'
    }
    response = client.put("/api/v1/users/me/password",json=request_body)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid(test_user):
    request_body = {"password": "rakib1234", "new_password": "rakib12"}
    response = client.put("/api/v1/users/me/password", json=request_body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_change_password_user_invalid(test_user):
#     request_body = {"password": "rakib1234", "new_password": "rakib12"}
#     response = client.put("/api/v1/users/me/password", json=request_body)
#     assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_phone_number(test_user):
    request_body = {"new_phone_number": "54362546385436"}
    response = client.put("/api/v1/users/me/phone", json=request_body)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_phone_number_already_used(test_user):
    request_body = {"new_phone_number": "9832760260"}
    response = client.put("/api/v1/users/me/phone", json=request_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_email(test_user):
    request_body = {"new_email": "rakib_18@gmail.com"}
    response = client.put("/api/v1/users/me/email", json=request_body)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_email_invalid(test_user):
    request_body = {"new_email": "rakib_18@mail.com"}
    response = client.put("/api/v1/users/me/email", json=request_body)
    assert response.json()['detail'][0]['msg'] == "Value error, Only gmail are allowed!"
