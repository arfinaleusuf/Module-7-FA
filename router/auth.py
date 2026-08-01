from fastapi import FastAPI, APIRouter,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Users
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from typing import Annotated
from database import SessionLocal
router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUsers(BaseModel):
    email : str
    username : str
    firstname : str
    lastname : str
    password : str
    role : str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/createuser')
def createuser(db: db_dependency, new_user: CreateUsers):
    user_model = Users(
        email = new_user.email,
        username = new_user.username,
        firstname = new_user.firstname,
        lastname = new_user.lastname,
        hash_password = bcrypt_context.hash(new_user.password),
        is_active = True,
        role = new_user.role
    )
    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=201, content={'messege': 'User added Successfully'})