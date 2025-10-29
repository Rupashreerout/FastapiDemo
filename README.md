🚀 HR Management FastAPI Backend

This is the FastAPI backend for the Eagles Performance & Reward Management System, providing REST APIs for employee management, attendance tracking, and authentication.

🏗️ Project Structure
EaglesApi/
├── main.py
├── database.py
├── models/
│   ├── employee.py
│   ├── attendance.py
│   └── user.py
├── routers/
│   ├── employees.py
│   ├── attendance.py
│   └── user.py
├── schemas/
│   ├── employee_schema.py
│   ├── attendance_schema.py
│   └── user_schema.py
├── requirements.txt
└── README.md

⚙️ 1. Clone Repository
git clone https://github.com/<your-username>/EaglesApi.git
cd EaglesApi

📦 2. Create Virtual Environment
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


macOS / Linux:

source venv/bin/activate

🧩 3. Install Dependencies
pip install -r requirements.txt


If requirements.txt doesn’t exist, generate it using:

pip freeze > requirements.txt

🛢️ 4. Setup Database (MySQL)
Create Database:
CREATE DATABASE eaglesdb;

Add .env File:

Create a .env file in the root directory:

DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
DB_NAME=eaglesdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

🧠 5. Configure Database Connection (database.py)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base: DeclarativeMeta = declarative_base()

👥 6. Employee Model (models/employee.py)
from sqlalchemy import Column, Integer, String
from fastapi_project.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    department = Column(String(100))
    designation = Column(String(100))

🕒 7. Attendance Model (models/attendance.py)
from sqlalchemy import Column, Integer, Date, ForeignKey
from fastapi_project.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date)
    status = Column(String(50))

🔐 8. Authentication (models/user.py)
from sqlalchemy import Column, Integer, String
from fastapi_project.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(50), default="Admin")

⚡ 9. Run Migrations (Create Tables)
uvicorn main:app --reload


Tables will auto-create if you have:

Base.metadata.create_all(bind=engine)


in your main file or individual models.

🧑‍💻 10. Run the Server
uvicorn main:app --reload


Visit your docs:
👉 http://127.0.0.1:8000/docs

🔑 11. API Routes Overview
Feature	Method	Endpoint	Description
Register User	POST	/user/register	Register new user
Login	POST	/user/login	Authenticate user
Get All Employees	GET	/employees/	Get all employees
Add Employee	POST	/employees/	Add new employee
Update Employee	PUT	/employees/{id}	Update employee info
Delete Employee	DELETE	/employees/{id}	Delete employee
Record Attendance	POST	/attendance/	Mark employee attendance
View Attendance	GET	/attendance/	Fetch attendance records
🧾 12. Git Commands

After creating your README.md, run:

git add README.md
git add .
git commit -m "Added FastAPI setup and documentation"
git push origin main
