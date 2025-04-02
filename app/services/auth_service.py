from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.db.models import User
from app.db.schemas import UserCreateDTO
import re

def register_user(user_data: UserCreateDTO, db: Session):
    # Validate email format
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not user_data.email or not re.match(email_regex, user_data.email):
        raise HTTPException(status_code=400, detail="Invalid or missing email")

    # Validate name (must not be empty)
    if not user_data.name or not user_data.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    # Check if user already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate password complexity
    password_regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not user_data.password or not re.match(password_regex, user_data.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long, include an uppercase letter, a number, and a special character"
        )

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, name=user_data.name.strip(), password=hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error saving user to database")

    return {"id": new_user.id, "email": new_user.email, "name": new_user.name, "created_at": new_user.created_at}

def login_user(email: str, password: str, db: Session):
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": create_access_token({"sub": user.email}),
        "refresh_token": create_refresh_token({"sub": user.email})
    }

def refresh_access_token(refresh_token: str):
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is required")

    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    email = payload.get("sub")
    return {
        "access_token": create_access_token({"sub": email}),
        "refresh_token": refresh_token
    }
