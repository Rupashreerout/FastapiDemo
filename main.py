from fastapi import FastAPI
from fastapi_project.router import user, login,employees,attendance
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(
    user.router,
    prefix="/user",
    tags=["user"]
)



app.include_router(
    login.router,
    prefix="/Login",
    tags=['Login']
)
app.include_router(
    employees.router,
    prefix="/Employees",
    tags=['Employees']
)

app.include_router(
    attendance.router,
    prefix="/Attendance",
    tags=['Attendance']
)