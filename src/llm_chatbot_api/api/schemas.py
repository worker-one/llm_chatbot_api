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

class InvokeChatbotRequest(BaseModel):
    user_id: int
    chat_id: int
    user_message: str
    chat_history_limit: Optional[int] = 10

class InvokeChatbotResponse(BaseModel):
    user_id: int
    chat_id: int
    ai_message: str

class AddUsersRequest(BaseModel):
    users: list[User]

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
