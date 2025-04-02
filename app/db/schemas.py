from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import enum
from datetime import datetime

class PrefixEnum(str, enum.Enum):
    mr = "Mr"
    ms = "Ms"
    miss = "Miss"

class UserRoleEnum(str, enum.Enum):
    user = "user"
    recruiter = "recruiter"

class UserCreateDTO(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)

class UserUpdateDTO(BaseModel):
    name: Optional[str]
    prefix: Optional[PrefixEnum]
    phone_number: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    nationality: Optional[str]

class UserResponseDTO(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRoleEnum
    created_at: datetime

    class Config:
        orm_mode = True

class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshDTO(BaseModel):
    refresh_token: str

class LoginDTO(BaseModel):
    email: EmailStr
    password: str


