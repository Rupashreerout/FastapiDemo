from fastapi_project.database import db_dependency,engine
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter,status,WebSocket,WebSocketDisconnect,Depends,BackgroundTasks
from pydantic import BaseModel,Field,EmailStr,validator
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_project.database import SessionLocal, engine
from typing import Optional
import enum
from sqlalchemy import Column, String, DateTime, Boolean, func, Text, Enum as SQLAlchemyEnum, ForeignKey
from uuid import uuid4, UUID
import uuid