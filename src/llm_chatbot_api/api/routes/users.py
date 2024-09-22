import logging

from fastapi import APIRouter, HTTPException
from omegaconf import OmegaConf
from sqlalchemy.orm import Session

from llm_chatbot_api.api import schemas
from llm_chatbot_api.db import models
from llm_chatbot_api.db.crud import read_users, upsert_user


# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/users")
def add_user(request: schemas.AddUserRequest):
    user = request.user

    logger.info(f"Adding user: {user}")
    upsert_user(user.id, user.name)
    return {"message": f"User `{user.name}` added successfully."}

@router.get("/users")
def get_users() -> list[schemas.User]:
    db_users = read_users()
    users = [schemas.User(id=db_user.id, name=db_user.name) for db_user in db_users]
    return users

@router.get("/users/{user_id}")
def get_user(user_id: int) -> schemas.User:
    db_users = read_users()
    users = [schemas.User(id=db_user.id, name=db_user.name) for db_user in db_users if user_id==db_user.id]
    if not users:
        raise HTTPException(status_code=404, detail=f"User `user_id` not found")
    return schemas.User(id=users[0].id, name=users[0].name)
