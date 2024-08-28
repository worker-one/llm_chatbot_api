import logging
from fastapi import APIRouter
from omegaconf import OmegaConf
from sqlalchemy.orm import Session
from llm_chatbot_api.db.crud import read_users
from llm_chatbot_api.db.database import get_session
from llm_chatbot_api.db import models
from llm_chatbot_api.api import schemas


# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)

# Apply the logging configuration
logging.config.dictConfig(logging_config)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/add_users", operation_id="ADD-USERS")
def add_users(request: schemas.AddUsersRequest):
    db: Session = get_session()
    users = request.users
    for user in users:
        logger.info(f"Adding user: {user}")
        db_user = models.User(id=user.id, name=user.name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return {"message": "Users added successfully."}

@router.get("/get_users", operation_id="GET-USERS")
def get_users() -> list[schemas.User]:
    db: Session = get_session()
    db_users = read_users(db)
    users = [schemas.User(id=db_user.id, name=db_user.name) for db_user in db_users]
    return users
