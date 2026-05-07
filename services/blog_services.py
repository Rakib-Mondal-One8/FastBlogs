from models import Blogs
from fastapi import HTTPException,status
import shutil, uuid
from sqlalchemy import func


def save_file(file):
    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = f"uploads/{file_name}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def create_blog(user, db, title, content,category,author, file):

    new_blog = Blogs(
        title=title,
        content=content,
        author=author,
        category=func.lower(category),
        image_url=save_file(file),
        user_id=user.get("user_id"),
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def update_blog(user, db, blog, blog_id, file):
    existing = (
        db.query(Blogs)
        .filter(Blogs.id == blog_id)
        .filter(Blogs.user_id == user.get("user_id"))
        .first()
    )

    if existing is None:
        raise HTTPException(status_code=404, detail="Blog Not Found!")

    existing.title = blog.title
    existing.content = blog.content
    existing.author = blog.author
    existing.category = blog.category
    existing.image_url = save_file(file)

    db.add(existing)
    db.commit()
    db.refresh(existing)


def delete_blog(user,db, blog_id):
    existing = (
        db.query(Blogs)
        .filter(Blogs.id == blog_id)
        .filter(Blogs.user_id == user.get("user_id"))
        .first()
    )

    if existing is None:
        raise HTTPException(status_code=404, detail="Blog Not Found!")

    db.delete(existing)
    db.commit()
