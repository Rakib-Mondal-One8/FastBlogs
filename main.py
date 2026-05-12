from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from routers import blogs,auth,users,admin,pages,readers
from database import Base,engine
from contextlib import asynccontextmanager
from services.cache_service import redis

app = FastAPI()



Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def life_span(app:FastAPI):
    await redis.connect()
    yield
    await redis.disconnect()

app.router.lifespan_context = life_span

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")
app.mount("/static",StaticFiles(directory="static"),name='static')




@app.get('/healthy')
def health_check(request:Request):
    return {'status':'Healthy'}


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(readers.router)
app.include_router(blogs.router)
app.include_router(pages.router)