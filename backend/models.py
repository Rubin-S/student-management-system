# backend/models.py
import enum 
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship 
from .database import Base
from datetime import datetime

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

    submissions = relationship("Submission", back_populates="student")


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

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course")
    submissions = relationship("Submission", back_populates="assignment")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    submission_date = Column(DateTime)
    file_path = Column(String) # Path to the stored file

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    score = Column(Float)
    comments = Column(String, nullable=True)

    assignment = relationship("Assignment")
    student = relationship("Student")

# --- NEW: MilestoneStatus Enum ---
class MilestoneStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# --- NEW: ResearchProject Model ---
class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    student_id = Column(Integer, ForeignKey("students.id"))

    student = relationship("Student")
    milestones = relationship("Milestone", back_populates="project")

# --- NEW: Milestone Model ---
class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    due_date = Column(Date)
    status = Column(Enum(MilestoneStatus), default=MilestoneStatus.PENDING)
    project_id = Column(Integer, ForeignKey("research_projects.id"))

    project = relationship("ResearchProject", back_populates="milestones")

# --- NEW: AuditLog Model ---
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    details = Column(String, nullable=True)

    user = relationship("User")