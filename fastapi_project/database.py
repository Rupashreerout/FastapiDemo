# from fastapi import Depends
# from typing import Annotated
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta
# from sqlalchemy.orm import sessionmaker,Session

# DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/fastapidemo"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# BASE = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session,Depends(get_db)]

from fastapi import Depends
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql+psycopg2://postgres:2001@localhost:5432/fastapidemo"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

BASE = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


