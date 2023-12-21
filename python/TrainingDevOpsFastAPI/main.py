import os
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DATABASE_URL = "mysql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + ":3306/" + DB_DATABASE
engine = create_engine(DATABASE_URL)

Base = declarative_base()
metadata = MetaData()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    email = Column(String(50), index=True)
    password = Column(String(50))

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(UserCreate):
    id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/v1/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/api/v1/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/v1/ping")
def ping():
    return {"ping": "pong"}

@app.post("/api/v1/auth/login")
def login():
    return {"message": "Login successful"}
