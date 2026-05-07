from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_token] = override_verify_token

def test_add_reader():
    request_body={
        'email': "rewijr@gmail.com"
    }
    response = client.post("/api/v1/readers",json=request_body)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_add_reader_invalid_email():
    request_body = {"email": "rewijr@google.com"}
    response = client.post("/api/v1/readers", json=request_body)
    print(response.json())
    assert response.json()["detail"][0]["msg"] == "Value error, Only gmail are allowed!"
