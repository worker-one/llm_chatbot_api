from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_chatbot'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    chats = relationship("Chat", back_populates="users_chatbot")

class Chat(Base):
    __tablename__ = 'chats_chatbot'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    timestamp = Column(DateTime)
    user = relationship("User", back_populates="chats_chatbot")

class Message(Base):
    __tablename__ = 'messages_chatbot'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    role = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)
    chat = relationship("Chat", back_populates="messages_chatbot")
