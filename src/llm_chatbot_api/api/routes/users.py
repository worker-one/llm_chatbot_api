import logging

from fastapi import APIRouter
from llm_chatbot_api.api import schemas
from llm_chatbot_api.db import models
from llm_chatbot_api.db.crud import read_user, upsert_user, read_users, delete_user
from omegaconf import OmegaConf
from sqlalchemy.orm import Session
from fastapi import HTTPException


# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/add_user")
def add_user(request: schemas.AddUserRequest):
    user = request.user

    logger.info(f"Adding user: {user}")
    upsert_user(user.id, user.name)
    return {"message": f"User `{user.name}` added successfully."}

@router.get("/user_exists")
def get_users(user_id: int) -> dict[str, bool]:
    db_user = read_user(user_id)
    if not db_user:
        return {"response": False}
    else:
        return {"response": True}

@router.get("/get_users")
def get_users() -> list[schemas.User]:
    db_users = read_users()
    users = [schemas.User(id=db_user.id, name=db_user.name) for db_user in db_users]
    return users

@router.post("/delete_user")
def remove_user(user_id: int):
    logger.info(f"Deleting user with id: {user_id}")
    try:
        # Call the delete_user function from the CRUD module
        delete_user(user_id)
        return {"message": f"User with id `{user_id}` deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting user with id {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting user with id `{user_id}`.")