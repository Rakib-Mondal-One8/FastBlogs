from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import blogs,auth,user,admin
from database import Base,engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(blogs.router)
