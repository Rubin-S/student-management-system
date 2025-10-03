# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from datetime import timedelta, datetime, date
from typing import List

from fastapi import Response
from ics import Calendar, Event

from . import models, schemas, auth
from .database import engine, get_db

from fastapi import UploadFile, File, Form
import shutil
import uuid
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .config import settings

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

# --- Email Configuration ---
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
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
# backend/main.py
# ...

@app.get("/seed-db/", status_code=status.HTTP_200_OK)
def seed_database(
    db: Session = Depends(get_db)
):
    """
    Populates the database with a rich set of sample data.
    Deletes existing data before adding new records.
    """
    current_user: models.User = Depends(auth.get_current_user)
    # 1. Clear existing data in the correct order to avoid foreign key errors
    db.query(models.Attendance).delete()
    db.query(models.Submission).delete()
    db.query(models.Session).delete()
    db.query(models.Assignment).delete()
    db.query(models.Student).delete()
    db.query(models.Course).delete()
    db.query(models.User).delete()
    db.commit()

    # 2. Create a default user
    hashed_password = auth.get_password_hash("adminpass")
    default_user = models.User(email="admin@example.com", hashed_password=hashed_password)
    db.add(default_user)

    # 3. Create students
    student1 = models.Student(first_name="Alice", last_name="Wonderland", email="alice@example.com")
    student2 = models.Student(first_name="Bob", last_name="Builder", email="bob@example.com")
    student3 = models.Student(first_name="Charlie", last_name="Chocolate", email="charlie@example.com")
    student4 = models.Student(first_name="Diana", last_name="Prince", email="diana@example.com")
    db.add_all([student1, student2, student3, student4])

    # 4. Create courses
    course1 = models.Course(title="Introduction to Python", code="CS101", description="A beginner's course.")
    course2 = models.Course(title="Web Development with FastAPI", code="CS205", description="Building modern web APIs.")
    course3 = models.Course(title="Advanced Algorithms", code="CS501", description="Deep dive into algorithms.")
    db.add_all([course1, course2, course3])

    # Commit users, students, and courses to get their IDs
    db.commit()

    # 5. Create assignments for courses
    assignment1 = models.Assignment(title="Basic Syntax Quiz", due_date=datetime(2025, 10, 15, 23, 59), course_id=course1.id)
    assignment2 = models.Assignment(title="First API Project", due_date=datetime(2025, 11, 1, 23, 59), course_id=course2.id)
    db.add_all([assignment1, assignment2])

    # 6. Create sessions for courses
    session1 = models.Session(date=date(2025, 10, 5), topic="Variables and Types", course_id=course1.id)
    session2 = models.Session(date=date(2025, 10, 12), topic="Loops and Conditionals", course_id=course1.id)
    session3 = models.Session(date=date(2025, 10, 8), topic="Path Parameters", course_id=course2.id)
    db.add_all([session1, session2, session3])

    # Commit assignments and sessions to get their IDs
    db.commit()

    # 7. Create a submission for an assignment
    submission1 = models.Submission(
        assignment_id=assignment1.id, 
        student_id=student1.id, 
        submission_date=datetime.now(),
        file_path="uploads/dummy_submission.pdf"
    )
    db.add(submission1)

    # 8. Mark attendance for a session
    attendance_records = [
        models.Attendance(session_id=session1.id, student_id=student1.id, status="present"),
        models.Attendance(session_id=session1.id, student_id=student2.id, status="present"),
        models.Attendance(session_id=session1.id, student_id=student3.id, status="absent"),
        models.Attendance(session_id=session1.id, student_id=student4.id, status="late"),
    ]
    db.add_all(attendance_records)

    # Final commit for submissions and attendance
    db.commit()

    return {"detail": "Database has been seeded with a rich set of sample data."}

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

# --- ASSIGNMENT & SUBMISSION ENDPOINTS ---
@app.post("/courses/{course_id}/assignments/", response_model=schemas.Assignment, status_code=status.HTTP_201_CREATED)
def create_assignment_for_course(
    course_id: int,
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_assignment = models.Assignment(**assignment.model_dump(), course_id=course_id)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@app.post("/assignments/{assignment_id}/submissions/", response_model=schemas.Submission, status_code=status.HTTP_201_CREATED)
def create_submission_for_assignment(
    assignment_id: int,
    student_id: int = Form(...), # Get student_id from form data
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # 1. Generate a unique filename to prevent conflicts
    unique_id = uuid.uuid4()
    file_extension = Path(file.filename).suffix
    unique_filename = f"{unique_id}{file_extension}"
    file_path = f"uploads/{unique_filename}"

    # 2. Save the file to the 'uploads' directory
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Create the submission record in the database
    db_submission = models.Submission(
        assignment_id=assignment_id,
        student_id=student_id,
        submission_date=datetime.now(),
        file_path=file_path
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

@app.get("/assignments/{assignment_id}/submissions/", response_model=List[schemas.SubmissionDetail])
def read_submissions_for_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    submissions = db.query(models.Submission).options(
        joinedload(models.Submission.student)
    ).filter(models.Submission.assignment_id == assignment_id).all()

    if submissions:
        print("DEBUG: First submission's student object:", submissions[0].student)
    
    return submissions

@app.get("/courses/{course_id}/assignments/", response_model=List[schemas.Assignment])
def read_assignments_for_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Retrieve all assignments for a specific course.
    """
    assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()
    
    return assignments

@app.get("/assignments/{assignment_id}", response_model=schemas.Assignment)
def read_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if db_assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment

# --- GRADEBOOK ENDPOINTS ---

@app.get("/courses/{course_id}/gradebook/", response_model=schemas.Gradebook)
def get_gradebook_for_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # NOTE: For a real app, you'd fetch students enrolled in the course. For now, we fetch all.
    students = db.query(models.Student).all()
    assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()

    # Get all student and assignment IDs for efficient filtering
    student_ids = [student.id for student in students]
    assignment_ids = [assignment.id for assignment in assignments]

    grades = db.query(models.Grade).filter(
        models.Grade.student_id.in_(student_ids),
        models.Grade.assignment_id.in_(assignment_ids)
    ).all()

    return {"students": students, "assignments": assignments, "grades": grades}

@app.post("/grades/", status_code=status.HTTP_200_OK)
def update_grades_bulk(
    update_data: schemas.BulkGradeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    for grade_data in update_data.grades:
        # Look for an existing grade for this student and assignment
        existing_grade = db.query(models.Grade).filter(
            models.Grade.student_id == grade_data.student_id,
            models.Grade.assignment_id == grade_data.assignment_id
        ).first()

        if existing_grade:
            # If found, update it
            existing_grade.score = grade_data.score
            existing_grade.comments = grade_data.comments
        else:
            # If not found, create a new grade record
            new_grade = models.Grade(**grade_data.model_dump())
            db.add(new_grade)

    db.commit()
    return {"detail": "Grades updated successfully"}

# --- Test Email Endpoint ---
@app.post("/email-test/")
async def send_test_email(
    current_user: models.User = Depends(auth.get_current_user)
):
    message = MessageSchema(
        subject="FastAPI Mail Test",
        recipients=[current_user.email],  # Send to the logged-in user's email
        body="<p>This is a test email sent from the Student Management System.</p>",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "Test email has been sent"}

@app.get("/assignments/{assignment_id}/ics")
def get_assignment_ics(
    assignment_id: int,
    db: Session = Depends(get_db)
    # No auth needed for this, as it's a public link
):
    db_assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Create a new calendar
    cal = Calendar()
    # Create an event for the assignment due date
    event = Event()
    event.name = f"Due: {db_assignment.title}"
    event.begin = db_assignment.due_date
    event.description = db_assignment.description

    # Add the event to the calendar
    cal.events.add(event)

    # Return the calendar as a downloadable file
    return Response(
        content=str(cal),
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=assignment_{assignment_id}.ics"}
    )

# --- RESEARCH & MILESTONE ENDPOINTS ---

@app.post("/students/{student_id}/projects/", response_model=schemas.ResearchProject, status_code=status.HTTP_201_CREATED)
def create_project_for_student(
    student_id: int,
    project: schemas.ResearchProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_project = models.ResearchProject(**project.model_dump(), student_id=student_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/students/{student_id}/projects/", response_model=List[schemas.ResearchProject])
def read_projects_for_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    projects = db.query(models.ResearchProject).filter(models.ResearchProject.student_id == student_id).all()
    return projects

@app.post("/projects/{project_id}/milestones/", response_model=schemas.Milestone, status_code=status.HTTP_201_CREATED)
def create_milestone_for_project(
    project_id: int,
    milestone: schemas.MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_milestone = models.Milestone(**milestone.model_dump(), project_id=project_id)
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@app.get("/projects/{project_id}/milestones/", response_model=List[schemas.Milestone])
def read_milestones_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    milestones = db.query(models.Milestone).filter(models.Milestone.project_id == project_id).all()
    return milestones

@app.put("/milestones/{milestone_id}", response_model=schemas.Milestone)
def update_milestone(
    milestone_id: int,
    milestone: schemas.MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_milestone = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    for var, value in milestone.model_dump().items():
        setattr(db_milestone, var, value)

    db.commit()
    db.refresh(db_milestone)
    return db_milestone