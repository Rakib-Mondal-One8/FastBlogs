from fastapi import APIRouter,status
from core.dependencies import db_dependency
from fastapi import Form
from schemas import ReaderCreate
from services import reader_services
from models import Readers

router = APIRouter(
    prefix='/api/v1/readers',
    tags=['Readers']
)


@router.post('',status_code=status.HTTP_204_NO_CONTENT)
async def add_reader(db:db_dependency,request_email:ReaderCreate):
    return reader_services.add_reader(db,request_email)
