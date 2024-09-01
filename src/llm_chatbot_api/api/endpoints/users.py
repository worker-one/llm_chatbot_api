import logging

from fastapi import APIRouter
from llm_chatbot_api.api import schemas
from llm_chatbot_api.db import models
from llm_chatbot_api.db.crud import read_user, read_users
from omegaconf import OmegaConf
from sqlalchemy.orm import Session

# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/add_user", operation_id="ADD-USER")
def add_user(request: schemas.AddUserRequest):
    user = request.user

    logger.info(f"Adding user: {user}")
    upsert_user(user.name)
    return {"message": f"User {user.name} added successfully."}

@router.get("/get_users", operation_id="GET-USERS")
def get_users() -> list[schemas.User]:
    db_users = read_users()
    users = [schemas.User(id=db_user.id, name=db_user.name) for db_user in db_users]
    return users
