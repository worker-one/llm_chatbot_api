from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    chat_id: str
    role: str
    content: str
    timestemp: datetime

class User(BaseModel):
    id: int
    name: str

class Chat(BaseModel):
    user_id: int
    chat_id: int
    chat_name: str

class QueryChatbotRequest(BaseModel):
    user_id: int
    chat_id: int
    user_message: str
    chat_history_limit: Optional[int] = 10

class QueryChatbotResponse(BaseModel):
    user_id: int
    chat_id: int
    ai_message: str

class AddUserRequest(BaseModel):
    user: User

class AddChatRequest(BaseModel):
    user_id: int
    chat_name: str

class DeleteChatRequest(BaseModel):
    user_id: int
    chat_id: int

class DeleteChatResponse(BaseModel):
    chat_id: int

class GetChatsRequest(BaseModel):
    user_id: int

class GetChatsResponse(BaseModel):
    chats: list[Chat]

class ModelInfoResponse(BaseModel):
    model_name: str
    provider: str
    max_tokens: int
    chat_history_limit: int
    temperature: float

class SetModelRequest(BaseModel):
    model_name: Optional[str] = None
    max_tokens: Optional[int] = None
    chat_history_limit: Optional[int] = None
    temperature: Optional[float] = None
