from pydantic import BaseModel, Field, field_validator
from re import compile, Pattern
from typing import Optional, ClassVar
from datetime import datetime


class BaseUserScheme(BaseModel):

    USERNAME_REGEX: ClassVar[Pattern] = compile(r"^[A-Za-z0-9_]+$")
    EMAIL_REGEX: ClassVar[Pattern] = compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+$")
    PASSWORD_REGEX: ClassVar[Pattern] = compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

    email: str = Field(..., max_length=50)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


    @field_validator("username")
    def validate_username(cls, v: str) -> str:
        if not cls.USERNAME_REGEX.match(v):
            raise ValueError(
                "Username must be 3-20 characters long and contain only letters, numbers, or underscores"
            )
        return v
    

    @field_validator("email")
    def validate_username(cls, v: str) -> str:
        if not cls.EMAIL_REGEX.match(v):
            raise ValueError(
                "Invalid email format"
            )
        
        return v
    
    @field_validator("password")
    def validate_password(cls, v: str) -> str:

        if not cls.PASSWORD_REGEX.match(v):
            raise ValueError(
                "Password must be at least 8 characters long, include uppercase, lowercase, number, and special character"
            )
        
        return v
    

class UpdateUserScheme(BaseUserScheme):

    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None



class UserOutScheme(BaseModel):
    id: Optional[int] = Field(..., gt=0)
    email: Optional[str] = Field(..., max_length=50)
    username: Optional[str] = Field(..., min_length=3, max_length=50)
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    



