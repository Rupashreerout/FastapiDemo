from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel
from .basic_import import *
from jose import jwt
from typing import List
from fastapi_project.models.user import User,Submission,Assignment
from passlib.hash import bcrypt
from fastapi_project.database import SessionLocal, engine
from datetime import datetime

SECRET_KEY = "secret"
router = APIRouter()


# Pydantic Models
class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: datetime

class AssignmentOut(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime

    class Config:
        orm_mode = True

class SubmissionCreate(BaseModel):
    content: str

class SubmissionOut(BaseModel):
    id: int
    content: str
    submitted_at: datetime
    student_id: int

    class Config:
        orm_mode = True

# Auth: Get current user from token
def get_current_user(db: Session = Depends(db_dependency), token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        user = db.query(User).filter(User.id == payload["id"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@router.post("/")
def create_assignment(data: AssignmentCreate, db: Session = Depends(db_dependency), user: User = Depends(get_current_user)):
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    assignment = Assignment(**data.dict(), teacher_id=user.id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return {"message": "Assignment created"}

@router.post("/{assignment_id}/submit")
def submit_assignment(assignment_id: int, submission: SubmissionCreate, db: Session = Depends(db_dependency), user: User = Depends(get_current_user)):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can submit assignments")
    new_submission = Submission(content=submission.content, assignment_id=assignment_id, student_id=user.id)
    db.add(new_submission)
    db.commit()
    return {"message": "Submitted successfully"}

@router.get("/{assignment_id}/submissions", response_model=List[SubmissionOut])
def view_submissions(assignment_id: int, db: Session = Depends(db_dependency), user: User = Depends(get_current_user)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment or assignment.teacher_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view submissions")
    submissions = db.query(Submission).filter(Submission.assignment_id == assignment_id).all()
    return submissions
