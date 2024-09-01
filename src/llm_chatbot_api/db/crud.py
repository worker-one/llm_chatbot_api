import logging
from datetime import datetime
from omegaconf import OmegaConf
from llm_chatbot_api.db.database import get_session
from llm_chatbot_api.db.models import Chat, Message, User
from sqlalchemy.orm import Session


# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("./src/llm_chatbot_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def read_user(user_id: int) -> User:
    db: Session = get_session()
    result = db.query(User).filter(User.id == user_id).first()
    db.close()
    return result

def read_users() -> list[User]:
    db: Session = get_session()
    result = db.query(User).all()
    db.close()
    return result

def get_user_chats(user_id: int) -> list[Chat]:
    db: Session = get_session()
    result = db.query(Chat).filter(Chat.user_id == user_id).all()
    db.close()
    return result

def get_chat_history(chat_id: int, limit: int = 10) -> list[Message]:
    db: Session = get_session()
    result = db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(Message.timestamp.asc()).limit(limit).all()
    db.close()
    return result


def upsert_user(user_id: int, name: str):
    db: Session = get_session()
    try:
        user = db.query(User).filter(User.name == name, User.id == user_id).first()
        if user:
            user.name = name
            user.id = user_id
            logger.info(f"User with id {name} updated successfully.")
        else:
            new_user = User(id = user_id, name=name)
            db.add(new_user)
            logger.info(f"User with name {name} added successfully.")
        db.commit()
    finally:
        db.close()

def create_chat(user_id: int, name: str) -> Chat:
    db: Session = get_session()
    db_chat = Chat(user_id=user_id, name=name)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    db.close()
    return db_chat

def delete_chat(user_id: int, chat_id: int) -> None:
    db: Session = get_session()
    # First, delete the messages associated with the chat
    db_messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    for message in db_messages:
        db.delete(message)

    # Then, delete the chat
    db_chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()
    db.delete(db_chat)
    db.commit()
    db.close()

def create_message(chat_id: int, role: str, content: str, timestamp: datetime) -> Message:
    db: Session = get_session()
    db_message = Message(chat_id=chat_id, role=role, content=content, timestamp=timestamp)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    db.close()
    return db_message
