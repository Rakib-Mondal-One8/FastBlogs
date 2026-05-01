from fastapi import HTTPException,status

from models import Blogs

import uuid,shutil

def save_file(file):

    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = f"uploads/{file_name}"

    with open(file_path,'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)

    return file_path

def update_blog(user,db,blog,blog_id,file):

    if(user.get('role')!='admin'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not an Admin!")

    existing = db.query(Blogs).filter(Blogs.id == blog_id).first()

    if existing is None:
        raise HTTPException(status_code=404, detail="Blog Not Found!")

    existing.title = blog.title
    existing.content = blog.content
    existing.author = blog.author
    existing.image_url = save_file(file)

    db.add(existing)
    db.commit()
    db.refresh(existing)


def delete_blog(user,db, blog_id):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not an Admin!"
        )

    existing = db.query(Blogs).filter(Blogs.id == blog_id).first()

    if existing is None:
        raise HTTPException(status_code=404, detail="Blog Not Found!")

    db.delete(existing)
    db.commit()
