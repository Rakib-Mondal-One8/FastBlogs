from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import blogs,auth,users,admin
from database import Base,engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(blogs.router)
