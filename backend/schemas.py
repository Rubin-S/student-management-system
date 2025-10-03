# backend/schemas.py
from pydantic import BaseModel, EmailStr,  Field
from typing import Optional, List
from datetime import date, datetime 
from .models import AttendanceStatus
from .models import MilestoneStatus

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

# --- SESSION SCHEMAS ---
class SessionBase(BaseModel):
    date: date
    topic: str
    course_id: int

class SessionCreate(BaseModel):
    date: date
    topic: str

class Session(BaseModel):
    id: int
    date: date
    topic: str
    course_id: int
    class Config:
        from_attributes = True

# --- ATTENDANCE SCHEMAS ---
class AttendanceBase(BaseModel):
    student_id: int
    status: AttendanceStatus

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    session_id: int
    class Config:
        from_attributes = True

# --- Combined schema for displaying student attendance ---
class StudentAttendance(BaseModel):
    student: Student # Use the existing Student schema
    status: Optional[AttendanceStatus] = None

class BulkAttendanceUpdate(BaseModel):
    attendances: List[AttendanceCreate]

# --- ASSIGNMENT SCHEMAS ---
class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    course_id: int
    class Config:
        from_attributes = True

# --- SUBMISSION SCHEMAS ---
class Submission(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submission_date: datetime
    file_path: str

    class Config:
        from_attributes = True

# --- Combined schema for displaying submission details ---
class SubmissionDetail(Submission): 
    student: Student 

# --- GRADE SCHEMAS ---
class GradeBase(BaseModel):
    assignment_id: int
    student_id: int
    score: float
    comments: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    class Config:
        from_attributes = True

# --- Schema for the bulk grade update request ---
class BulkGradeUpdate(BaseModel):
    grades: List[GradeCreate]

# --- Schema for the complete gradebook response ---
class Gradebook(BaseModel):
    students: List[Student]
    assignments: List[Assignment]
    grades: List[Grade]

# --- RESEARCH PROJECT SCHEMAS ---
class ResearchProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None

class ResearchProjectCreate(ResearchProjectBase):
    pass

class ResearchProject(ResearchProjectBase):
    id: int
    student_id: int
    class Config:
        from_attributes = True

# --- MILESTONE SCHEMAS ---
class MilestoneBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: MilestoneStatus = MilestoneStatus.PENDING

class MilestoneCreate(MilestoneBase):
    pass

class Milestone(MilestoneBase):
    id: int
    project_id: int
    class Config:
        from_attributes = True