from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from starlette import status
from models import Readers, Blogs, Users
from core.dependencies import db_dependency,get_current_user_optional
from core.security import redirect_to_login

router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
def home_page(request: Request,db: db_dependency,user:dict|None = Depends(get_current_user_optional)):
    readers = db.query(Readers).count()
    blogs = db.query(Blogs).count()
    users = db.query(Users).count()
    return templates.TemplateResponse(
        request, "home.html", {"readers": readers, "blogs": blogs, "writers": users,"user":user}
    )


@router.get("/blogs", status_code=status.HTTP_200_OK)
async def read_blogs(
    request: Request,
    db: db_dependency,
    user = Depends(get_current_user_optional),
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
            {"blogs": blogs,"page":page, "limit": limit, "total_pages": total_pages,'category':'all',"user":user},
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
def read_blog_details(request:Request,db:db_dependency,user = Depends(get_current_user_optional),blog_id:int=Path(gt=0)):
    # user = get_current_user_optinal()
    blog = db.query(Blogs).filter(Blogs.id==blog_id).first()
    return templates.TemplateResponse(request,'details.html',{'blog':blog,"user":user})

@router.get("/categories")
def categories_page(request: Request,db:db_dependency,user = Depends(get_current_user_optional)):
    # user = get_current_user_optinal()
    fastapi_articles = db.query(Blogs).filter(Blogs.category=='fastapi').count()
    security_articles = db.query(Blogs).filter(Blogs.category=='security').count()
    database_articles = db.query(Blogs).filter(Blogs.category=='database').count()
    deployment_articles = db.query(Blogs).filter(Blogs.category=='deployment').count()
    system_design_articles = db.query(Blogs).filter(Blogs.category=='system design').count()
    apis_articles = db.query(Blogs).filter(Blogs.category=='apis').count()
    articles = {
        'fastapi_count':fastapi_articles,
        'security_count':security_articles,
        'databases_count':database_articles,
        'deployment_count':deployment_articles,
        'system_design_count':system_design_articles,
        'apis_count':apis_articles
    }
    return templates.TemplateResponse(request, "categories.html",{'articles':articles,"user":user})


@router.get("/categories/{topic}")
def categories_topic_page(request:Request,db:db_dependency,topic:str,user = Depends(get_current_user_optional),):
    # user = get_current_user_optinal()
    category = topic.lower()
    blogs = db.query(Blogs).filter(Blogs.category==category).all()
    return templates.TemplateResponse(request,"topics.html",{'blogs':blogs,'topic':topic,"user":user})

@router.get("/about")
def about_page(request: Request,user = Depends(get_current_user_optional)):
    # user = get_current_user_optinal()
    return templates.TemplateResponse(request, "about.html",{"user":user})



@router.get("/profile/{username}")
def profile_page(request:Request,db:db_dependency,user = Depends(get_current_user_optional)):
    # user = get_current_user_optinal()
    if not user: return redirect_to_login()

    user_info = db.query(Users).filter(Users.id==user.get('user_id')).first()
    return templates.TemplateResponse(request,'profile.html',{'user':user_info})


@router.get("/auth/register")
def registration_page(request:Request):
    return templates.TemplateResponse(request,'register.html')


@router.get("/auth/login")
def login_page(request:Request):
    return templates.TemplateResponse(request,'login.html')


@router.get("/logout")
def logout_page(request:Request):
    return redirect_to_login()