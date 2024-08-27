from fastapi import APIRouter
from sqlalchemy.orm import Session
from llm_chatbot_api.db.crud import get_users
from llm_chatbot_api.db.database import get_session

router = APIRouter()

@router.get("/")
def read_users():
    db: Session = get_session()
    users = get_users(db)
    return users
