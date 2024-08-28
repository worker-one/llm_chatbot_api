from fastapi import APIRouter
from sqlalchemy.orm import Session
from llm_chatbot_api.db.crud import read_users
from llm_chatbot_api.db.database import get_session
from llm_chatbot_api.api.schemas import AddUsersRequest, User

router = APIRouter()

@router.post("/add_users", operation_id="ADD-USERS")
def add_users(request: AddUsersRequest):
    db: Session = get_session()
    users = request.users
    for user in users:
        db_user = User(id=user.id, name=user.name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return {"message": "Users added successfully."}

@router.get("/get_users", operation_id="GET-USERS")
def get_users() -> list[User]:
    db: Session = get_session()
    users = read_users(db)
    return users
