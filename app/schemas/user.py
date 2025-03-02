from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_digits=50)
    email: EmailStr
    username: str
    username: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_digits=50)


class UserResponse(UserBase):
    user_id: int
