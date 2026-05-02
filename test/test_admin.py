from .utils import *


def test_update_blog(test_blog):
    request_body = {
        "title": "New Blog 1",
        "content": "THis is a New Blog 1",
        "author": "Rakib",
    }
    files = {"file": ("test.png", b"dummy data", "image/png")}
    response = client.put("/api/v1/admin/blogs/1", data=request_body, files=files)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_blog_invalid(test_blog):
    request_body = {
        "title": "New Blog 1",
        "content": "THis is a New Blog 1",
        "author": "Rakib",
    }
    files = {"file": ("test.png", b"dummy data", "image/png")}
    response = client.put("/api/v1/admin/blogs/999", data=request_body, files=files)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_blog(test_blog):
    response = client.delete("/api/v1/admin/blogs/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_blog_invalid(test_blog):
    response = client.delete("/api/v1/admin/blogs/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
