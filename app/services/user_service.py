from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import User
from app.db.schemas import UserUpdateDTO
import re

def get_user_profile(current_user: User):
    return current_user

def update_user_profile(update_data: UserUpdateDTO, db: Session, current_user: User):
    if update_data.name and not update_data.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if update_data.phone_number:
        phone_regex = r"^\+?[1-9]\d{1,14}$"
        if not re.match(phone_regex, update_data.phone_number):
            raise HTTPException(status_code=400, detail="Invalid phone number format")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)

    try:
        db.commit()
        db.refresh(current_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating user profile")

    return current_user

def add_user_by_recruiter(user_data: UserUpdateDTO, db: Session):
    if not user_data.email or not user_data.name:
        raise HTTPException(status_code=400, detail="Email and name are required")

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(**user_data.dict(), role="user")

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating user")

    return new_user

def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(user)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting user")

    return {"detail": "User deleted successfully"}
