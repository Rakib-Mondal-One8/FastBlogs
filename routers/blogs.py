from typing import Annotated
from fastapi import Depends, HTTPException, Path, Query
from starlette import status
from fastapi import APIRouter, UploadFile, File, Form
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import BlogCreate
from services import blog_services
import uuid, shutil
from models import Blogs
from core.dependencies import db_dependency, user_dependency

router = APIRouter(prefix="/api/v1/blogs", tags=["Blogs"])


@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    models = db.query(Blogs).all()
    return models


@router.get("/{blog_id}", status_code=status.HTTP_200_OK)
async def read_blog(
    user: user_dependency, db: db_dependency, blog_id: int = Path(gt=0)
):
    print("Working3")
    blog = db.query(Blogs).filter(Blogs.id == blog_id).first()
    return blog


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_blog(
    user: user_dependency,
    db: db_dependency,
    title: str = Form(),
    content: str = Form(),
    author: str = Form(),
    category: str = Form(),
    file: UploadFile = File(),
):

    # Validating Inside because File() and Schemas doesn't work together
    try:
        blog = BlogCreate(
            title=title, content=content, author=author, category=category
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return blog_services.create_blog(
        user, db, blog.title, blog.content, blog.category, blog.author, file
    )


@router.put("/{blog_id}", status_code=status.HTTP_200_OK)
async def update_blog(
    user: user_dependency,
    db: db_dependency,
    title: str = Form(),
    content: str = Form(),
    author: str = Form(),
    category: str = Form(),
    file: UploadFile = File(),
    blog_id: int = Path(gt=0),
):
    try:
        blog = BlogCreate(
            title=title, content=content, author=author, category=category
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return blog_services.update_blog(user, db, blog, blog_id, file)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    user: user_dependency, db: db_dependency, blog_id: int = Path(gt=0)
):
    return blog_services.delete_blog(user, db, blog_id)
