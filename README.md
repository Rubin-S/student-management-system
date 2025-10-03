# Student Information System (SIS)

A full-stack web application for managing students, courses, attendance, assignments, and grades. This system is designed to provide a comprehensive solution for educators and administrators.

---

## ✨ Features

* **User Authentication**: Secure login system with JWT tokens.
* **Student & Course Management**: Full CRUD operations for students and courses.
* **Attendance Tracking**: Mark and track student attendance per class session.
* **Assignments & Submissions**: Create assignments and handle student file uploads.
* **Gradebook**: Enter and manage grades in a grid-style gradebook.
* **Calendar Export**: Export assignment due dates as ICS files for easy calendar integration.
* **Research Tracking**: Monitor student research projects and milestones.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, Python 3.10, SQLAlchemy (ORM), PostgreSQL (Production), SQLite (Development)
* **Frontend**: React (with Vite), JavaScript, Axios
* **DevOps**: Git, Docker (to be added)

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+ and Conda (or another virtual environment manager)
* Node.js and npm
* A running PostgreSQL instance (for production)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd student-management-system
    ```

2.  **Backend Setup:**
    ```bash
    # Navigate to the backend folder
    cd backend

    # Create and activate the conda environment
    conda create --name sis-env python=3.10
    conda activate sis-env

    # Install dependencies
    pip install -r requirements.txt  # We will create this file later

    # Create a .env file from the .env.example template
    # and fill in your credentials (e.g., for Mailtrap)
    cp .env.example .env
    ```

3.  **Frontend Setup:**
    ```bash
    # Navigate to the frontend folder from the root
    cd frontend

    # Install dependencies
    npm install
    ```

### Running the Application

1.  **Start the Backend Server:**
    * From the **root** directory, run:
    ```bash
    uvicorn backend.main:app --reload
    ```
    * The API will be available at `http://127.0.0.1:8000`.

2.  **Start the Frontend Server:**
    * In a **separate terminal**, from the `frontend` directory, run:
    ```bash
    npm run dev
    ```
    * The application will be available at `http://localhost:5173`.

---

## 📚 API Documentation

Once the backend server is running, interactive API documentation (Swagger UI) is automatically available at `http://127.0.0.1:8000/docs`.