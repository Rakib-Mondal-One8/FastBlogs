from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from routers import blogs,auth,users,admin,pages
from database import Base,engine


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")
app.mount("/static",StaticFiles(directory="static"),name='static')




@app.get('/healthy')
def health_check(request:Request):
    return {'status':'Healthy'}


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(pages.router)