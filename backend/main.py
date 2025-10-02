# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Information System API",
    description="API for managing students, courses, and grades.",
    version="0.1.0",
)

origins = [
    "http://localhost:5173", # The origin of our React app
    "http://localhost:5174", # Add other potential ports if needed
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Information System API"}

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and create the user
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find the user by email (form_data.username is the email)
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    # Check if user exists and password is correct
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create the access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# --- STUDENT CRUD ENDPOINTS ---

@app.post("/students/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students/", response_model=List[schemas.Student])
def read_students(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

# --- NEW: GET A SINGLE STUDENT ---
@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(
    student_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

# --- NEW: UPDATE A STUDENT ---
@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int, 
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update model instance with new data
    for var, value in student.model_dump().items():
        setattr(db_student, var, value)

    db.commit()
    db.refresh(db_student)
    return db_student

# --- NEW: DELETE A STUDENT ---
@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(
    student_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return {"detail": "Student deleted successfully"}

# --- COURSE CRUD ENDPOINTS ---

@app.post("/courses/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

@app.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@app.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(
    course_id: int,
    course: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    for var, value in course.model_dump().items():
        setattr(db_course, var, value)

    db.commit()
    db.refresh(db_course)
    return db_course

@app.delete("/courses/{course_id}", status_code=status.HTTP_200_OK)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(db_course)
    db.commit()
    return {"detail": "Course deleted successfully"}

# --- DEVELOPMENT: SEED DATABASE ---
@app.get("/seed-db/", status_code=status.HTTP_200_OK)
def seed_database(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Populates the database with initial sample data.
    Deletes existing students and courses before adding new ones.
    """
    # 1. Clear existing data
    db.query(models.Student).delete()
    db.query(models.Course).delete()
    db.commit()

    # 2. Create sample courses
    sample_courses = [
        models.Course(title="Introduction to Python", code="CS101", description="A beginner's course on Python programming."),
        models.Course(title="Web Development with FastAPI", code="CS205", description="Building modern web APIs."),
        models.Course(title="Database Systems", code="CS310", description="Fundamentals of SQL and database design."),
    ]
    db.add_all(sample_courses)
    db.commit()

    # 3. Create sample students
    sample_students = [
        models.Student(first_name="Alice", last_name="Smith", email="alice@example.com"),
        models.Student(first_name="Bob", last_name="Johnson", email="bob@example.com"),
        models.Student(first_name="Charlie", last_name="Brown", email="charlie@example.com"),
    ]
    db.add_all(sample_students)
    db.commit()

    return {"detail": "Database has been seeded with sample data."}

# --- SESSION & ATTENDANCE ENDPOINTS ---
@app.post("/courses/{course_id}/sessions/", response_model=schemas.Session, status_code=status.HTTP_201_CREATED)
def create_session_for_course(
    course_id: int,
    session: schemas.SessionCreate, # Use the new schema here
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_session = models.Session(**session.model_dump(), course_id=course_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@app.get("/courses/{course_id}/sessions/", response_model=List[schemas.Session])
def read_sessions_for_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Retrieve all sessions for a specific course.
    """
    sessions = db.query(models.Session).filter(models.Session.course_id == course_id).all()
    return sessions

# NOTE: For a real app, you'd fetch students enrolled in the course. For now, we fetch all students.
@app.get("/sessions/{session_id}/attendance/", response_model=List[schemas.StudentAttendance])
def get_attendance_for_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Fetch all students (in a real app, this would be students for the session's course)
    all_students = db.query(models.Student).all()

    # Fetch existing attendance records for this session
    attendance_records = db.query(models.Attendance).filter(models.Attendance.session_id == session_id).all()
    attendance_map = {record.student_id: record.status for record in attendance_records}

    # Combine student list with their attendance status
    response_data = []
    for student in all_students:
        response_data.append({
            "student": student,
            "status": attendance_map.get(student.id) # Will be None if not marked yet
        })
    return response_data

@app.post("/sessions/{session_id}/attendance/", status_code=status.HTTP_200_OK)
def update_attendance_for_session(
    session_id: int,
    update_data: schemas.BulkAttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    for att_data in update_data.attendances:
        # Check if an attendance record already exists for this student and session
        record = db.query(models.Attendance).filter(
            models.Attendance.session_id == session_id,
            models.Attendance.student_id == att_data.student_id
        ).first()

        if record:
            # If it exists, update the status
            record.status = att_data.status
        else:
            # If not, create a new record
            new_record = models.Attendance(
                session_id=session_id,
                student_id=att_data.student_id,
                status=att_data.status
            )
            db.add(new_record)

    db.commit()
    return {"detail": "Attendance updated successfully"}