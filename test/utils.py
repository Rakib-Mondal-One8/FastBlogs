from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from database import Base
from fastapi.testclient import TestClient
from main import app
from core.dependencies import get_db
from core.security import verify_token
from fastapi import status,HTTPException
from models import Users,Blogs
from core.security import pwd_context
from pytest import fixture
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_verify_token():
    return {"username":"RakibOne8","user_id":1,"role":'admin'}


client = TestClient(app)


@fixture
def test_user():
    db = TestingSessionLocal()
    user = Users(
        email="rakib@gmail.com",
        username="Rakib0ne8",
        first_name="Rakib",
        last_name="Mondal",
        role="admin",
        hashed_password=pwd_context.hash("rakib123"),
        phone_number='9832760260',
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@fixture
def test_blog():
    db = TestingSessionLocal()
    new_blog = Blogs(
        title="New Blog",
        content="This is the New Blog",
        author="Rakib",
        image_url="uploads/demo",
        user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    yield new_blog
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM blogs;"))
        connection.commit()
