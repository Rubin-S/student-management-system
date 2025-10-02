# backend/schemas.py
from pydantic import BaseModel, EmailStr,  Field
from typing import Optional

# Base model for a student
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

# Model for creating a new student
class StudentCreate(StudentBase):
    pass

# Model for reading a student (includes the ID)
class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True # Formerly orm_mode

# Schema for creating a user
class UserCreate(BaseModel):
    email: EmailStr
    # Add a Field with min_length and max_length validation
    password: str = Field(..., min_length=8, max_length=72)

# Schema for reading a user
class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# --- COURSE SCHEMAS ---

class CourseBase(BaseModel):
    title: str
    code: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True