from fastapi import APIRouter
from sqlalchemy.orm import Session
from .. import crud, models
from ..database import get_session

router = APIRouter()

@router.get("/")
def read_users():
    db: Session = get_session()
    users = crud.get_users(db)
    return users
