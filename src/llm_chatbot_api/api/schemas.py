from pydantic import BaseModel

class Message(BaseModel):
    chat_id: str
    role: str
    content: str

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

class InvokeChatbotResponse(BaseModel):
    user_id: int
    chat_id: str
    llm_message: str

class AddUsersRequest(BaseModel):
    users: list[User]

class AddChatRequest(BaseModel):
    user_id: int
    chat_name: str

class GetChatsRequest(BaseModel):
    user_id: int

class GetChatsResponse(BaseModel):
    chats: list[Chat]
