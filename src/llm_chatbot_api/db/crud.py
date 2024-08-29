from datetime import datetime

from llm_chatbot_api.db.models import Chat, Message, User
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session


def read_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def read_users(db: Session) -> list[User]:
    return db.query(User).all()

def get_user_chats(db: Session, user_id: int):
    return db.query(Chat).filter(Chat.user_id == user_id).all()

def get_chat_history(db: Session, user_id: int, chat_id: int, limit: int = 10) -> list[Message]:
    return db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(Message.timestamp.desc()).limit(limit).all()

def create_user(db: Session, name: str):
    db_user = User(name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_chat(db: Session, user_id: int, name: str):
    db_chat = Chat(user_id=user_id, name=name)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def delete_chat(db: Session, user_id: int, chat_id: int):
    # First, delete the messages associated with the chat
    db_messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    for message in db_messages:
        db.delete(message)

    # Then, delete the chat
    db_chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()
    db.delete(db_chat)
    db.commit()

def create_message(db: Session, chat_id: int, role: str, content: str, timestamp: datetime):
    db_message = Message(chat_id=chat_id, role=role, content=content, timestamp=timestamp)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
