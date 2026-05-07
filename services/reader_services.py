from models import Readers
from fastapi import HTTPException, status


def add_reader(db, request_email):
    existing = db.query(Readers).filter(Readers.email == request_email.email).first()
    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail="Reader already exists!",
        )

    reader = Readers(email=request_email.email)
    db.add(reader)
    db.commit()
    db.refresh(reader)
