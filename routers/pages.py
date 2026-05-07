from fastapi import APIRouter, HTTPException, Path, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from starlette import status
from models import Readers, Blogs, Users
from core.dependencies import db_dependency

router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
def home_page(request: Request, db: db_dependency):
    readers = db.query(Readers).count()
    blogs = db.query(Blogs).count()
    users = db.query(Users).count()
    return templates.TemplateResponse(
        request, "home.html", {"readers": readers, "blogs": blogs, "writers": users}
    )


@router.get("/blogs", status_code=status.HTTP_200_OK)
async def read_blogs(
    request: Request,
    db: db_dependency,
    category: str | None = Query(default=None),
    page: int = Query(default=1),
    limit: int = Query(default=3),
):
    discard = limit * (page - 1)
    query = db.query(Blogs)
    if category is None or category.lower() == "all":
        total_pages = (query.count() + limit-1) // limit
        blogs = query.offset(discard).limit(limit).all()
        return templates.TemplateResponse(
            request,
            "blogs.html",
            {"blogs": blogs,"page":page, "limit": limit, "total_pages": total_pages,'category':'all'},
        )

    total_pages = (
        query.filter(Blogs.category == func.lower(category)).count()+limit-1
    ) // limit
    blogs = (
        query
        .filter(Blogs.category == func.lower(category))
        .offset(discard)
        .limit(limit)
        .all()
    )
    # if not blogs:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Blogs not found on this category.",
    #     )
    return templates.TemplateResponse(
        request,
        "blogs.html",
        {
            "blogs": blogs,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "category": category,
        },
    )

@router.get("/blogs/details/{blog_id}")
def read_blog_details(request:Request,db:db_dependency,blog_id:int=Path(gt=0)):
    blog = db.query(Blogs).filter(Blogs.id==blog_id).first()
    return templates.TemplateResponse(request,'details.html',{'blog':blog})

@router.get("/categories")
def categories_page(request: Request):
    return templates.TemplateResponse(request, "categories.html")


@router.get("/categories/{topic}")
def categories_topic_page(request:Request,topic:str):
    return templates.TemplateResponse(request,"topics.html",{'topic':topic})

@router.get("/about")
def about_page(request: Request):
    return templates.TemplateResponse(request, "about.html")
