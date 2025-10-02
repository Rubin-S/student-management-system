# backend/models.py
import enum 
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey 
from sqlalchemy.orm import relationship 
from .database import Base

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    topic = Column(String, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course")
    attendance_records = relationship("Attendance", back_populates="session")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    status = Column(Enum(AttendanceStatus), nullable=False)

    session = relationship("Session", back_populates="attendance_records")
    student = relationship("Student")