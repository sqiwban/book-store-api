from datetime import date

from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict

from app.models import UserRole


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    bio: str | None = None
    birth_date: date

    @field_validator("birth_date")
    @classmethod
    def birth_date_not_in_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("birth_date cannot be in the future")
        return v

class AuthorCreate(AuthorBase):
    pass

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    price: int = Field(..., ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    price: int | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class OrderCreate(BaseModel):
    book_id: int
    quantity: int = Field(..., gt=0)

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: UserRole