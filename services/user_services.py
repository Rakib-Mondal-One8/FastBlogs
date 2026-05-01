from models import Users
from fastapi import HTTPException, status
from core.security import pwd_context


def verify_password(plain, hashed):
    if not pwd_context.verify(plain, hashed):
        return False
    return True


def get_user(user, db):
    user_data = db.query(Users).filter(Users.id == user.get("user_id")).first()
    return user_data


def change_password(user, db, password_change):
    existing = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found!"
        )

    if verify_password(password_change.password, existing.hashed_password):
        existing.hashed_password = pwd_context.hash(password_change.new_password)

        db.add(existing)
        db.commit()
        db.refresh(existing)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Given Password is Not Currect!",
        )


def update_phone_number(user, db, phone_number_change):
    existing = (
        db.query(Users)
        .filter(Users.phone_number == phone_number_change.new_phone_number)
        .filter(Users.id == user.get("user_id"))
        .first()
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone Number Already in use!",
        )

    model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    model.phone_number = phone_number_change.new_phone_number

    db.add(model)
    db.commit()
    db.refresh(model)


def update_email(user, db, email_update):
    existing = db.query(Users).filter(Users.id == user.get("user_id")).first()
    existing.email = email_update.new_email
    db.add(existing)
    db.commit()
    db.refresh(existing)
