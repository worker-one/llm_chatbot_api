from pydantic import BaseModel


class InvokeChatbotRequest(BaseModel):
    user_id: str
    chat_id: str
    user_message: str

class InvokeChatbotResponse(BaseModel):
    user_id: str
    chat_id: str
    llm_message: str

class Message(BaseModel):
    chat_id: str
    role: str
    content: str

class Chat(BaseModel):
    chat_id: str
    chat_name: str
    messages: list[Message]

class ChatsRequest(BaseModel):
    user_id: str

class ChatsResponse(BaseModel):
    chats: list[Chat]
