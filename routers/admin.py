from fastapi import APIRouter, HTTPException,status,UploadFile,Form,File,Path
from core.dependencies import db_dependency,user_dependency
from schemas import BlogCreate
from services import admin_services


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"]
) 


@router.put("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_blog(
    user: user_dependency,
    db: db_dependency,
    title: str = Form(),
    content: str = Form(),
    author: str = Form(),
    file: UploadFile = File(),
    blog_id: int = Path(gt=0),
):
    try:
        blog = BlogCreate(title=title, content=content, author=author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return admin_services.update_blog(user,db, blog, blog_id, file)


@router.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    user: user_dependency, db: db_dependency, blog_id: int = Path(gt=0)
):
    return admin_services.delete_blog(user,db, blog_id)
