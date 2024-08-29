import logging

from fastapi import APIRouter
from llm_chatbot_api.api import schemas
from llm_chatbot_api.db import models
from llm_chatbot_api.db.crud import read_user, read_users
from llm_chatbot_api.db.database import get_session
from omegaconf import OmegaConf
from sqlalchemy.orm import Session

# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/add_user", operation_id="ADD-USER")
def add_user(request: schemas.AddUserRequest):
    db: Session = get_session()
    user = request.user

    # Check if the user already exists
    db_user = read_user(db, user.id)
    if not db_user is None:
        return {"message": f"User {user.name} already exists."}

    logger.info(f"Adding user: {user}")
    db_user = models.User(id=user.id, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": f"User {user.name} added successfully."}

@router.get("/get_users", operation_id="GET-USERS")
def get_users() -> list[schemas.User]:
    db: Session = get_session()
    db_users = read_users(db)
    users = [schemas.User(id=db_user.id, name=db_user.name) for db_user in db_users]
    return users
