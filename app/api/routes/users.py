from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.db.schemas import UserUpdateDTO, UserResponseDTO
from app.core.security import get_current_user, require_recruiter
from app.services.user_service import get_user_profile, update_user_profile, add_user_by_recruiter, delete_user

router = APIRouter()

@router.get("/me", response_model=UserResponseDTO)
def get_profile(current_user: User = Depends(get_current_user)):
    return get_user_profile(current_user)

@router.put("/update", response_model=UserResponseDTO)
def update_profile(update_data: UserUpdateDTO, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return update_user_profile(update_data, db, current_user)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error during profile update")

@router.post("/add", response_model=UserResponseDTO)
def add_user(user_data: UserUpdateDTO, db: Session = Depends(get_db), recruiter: User = Depends(require_recruiter)):
    try:
        return add_user_by_recruiter(user_data, db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error during user creation")

@router.delete("/delete/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db), recruiter: User = Depends(require_recruiter)):
    try:
        return delete_user(user_id, db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error during user deletion")
