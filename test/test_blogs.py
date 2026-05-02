from .utils import *


def test_read_all(test_blog):

    response = client.get("/api/v1/blogs")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id':1,
        'title':"New Blog",
        'content':"This is the New Blog",
        'author':"Rakib",
        'image_url':"uploads/demo",
        'user_id':1
    }]


def test_read_blog(test_blog):
    response = client.get("/api/v1/blogs/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id':1,
        'title':"New Blog",
        'content':"This is the New Blog",
        'author':"Rakib",
        'image_url':"uploads/demo",
        'user_id':1
    }


def test_read_blog_invalid(test_blog):
    response = client.get("/api/v1/blogs/999")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == None


def test_create_blog():
    request_body = {
        'title':'New Blog 2',
        'content':'THis is a New Blog',
        'author':"Rakib",
    }
    files = {"file": ("test.png", b"dummy data", "image/png")}
    response = client.post("/api/v1/blogs",data=request_body,files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == 'New Blog 2'

    # if you're not using the test_blog fixture
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM blogs;"))
        connection.commit()


def test_update_blog(test_blog):
    request_body = {
        "title": "New Blog 1",
        "content": "THis is a New Blog 1",
        "author": "Rakib",
    }
    files = {"file": ("test.png", b"dummy data", "image/png")}
    response = client.put("/api/v1/blogs/1", data=request_body, files=files)
    assert response.status_code == status.HTTP_200_OK


def test_update_blog_invalid(test_blog):
    request_body = {
        "title": "New Blog 1",
        "content": "THis is a New Blog 1",
        "author": "Rakib",
    }
    files = {"file": ("test.png", b"dummy data", "image/png")}

    response = client.put("/api/v1/blogs/999", data=request_body, files=files)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_blog(test_blog):
    response = client.delete("/api/v1/blogs/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_blog_invalid(test_blog):
    response = client.delete("/api/v1/blogs/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND