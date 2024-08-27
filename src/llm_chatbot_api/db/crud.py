from llm_chatbot_api.db.models import Chat, Message, User
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

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

def create_chat(db: Session, user_id: int, message: str, timestamp):
    db_chat = Chat(user_id=user_id, message=message, timestamp=timestamp)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_message(db: Session, chat_id: int, role: str, message: str, timestamp):
    db_message = Message(chat_id=chat_id, role=role, message=message, timestamp=timestamp)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
