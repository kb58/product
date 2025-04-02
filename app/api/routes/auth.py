from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas import UserCreateDTO, TokenDTO, TokenRefreshDTO, LoginDTO,UserResponseDTO
from app.services.auth_service import register_user, login_user, refresh_access_token

router = APIRouter()

@router.post("/register",response_model=UserResponseDTO)
def register(user: UserCreateDTO, db: Session = Depends(get_db)):
    try:
        return register_user(user, db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error during registration")

@router.post("/login", response_model=TokenDTO)
def login(user: LoginDTO, db: Session = Depends(get_db)):
    try:
        return login_user(user.email, user.password, db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error during login")

@router.post("/refresh", response_model=TokenDTO)
def refresh_token(token_data: TokenRefreshDTO):
    try:
        return refresh_access_token(token_data.refresh_token)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error during token refresh")
