from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory='templates')

@router.get("/")
def home_page(request:Request):
    return templates.TemplateResponse(request,'home.html')

@router.get("/blogs")
def blogs_page(request:Request):
    return templates.TemplateResponse(request,'blogs.html')


@router.get("/categories")
def categories_page(request:Request):
    return templates.TemplateResponse(request,'categories.html')

@router.get("/about")
def about_page(request:Request):
    return templates.TemplateResponse(request,'about.html')