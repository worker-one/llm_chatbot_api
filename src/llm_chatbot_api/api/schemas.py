from pydantic import BaseModel

class Message(BaseModel):
    chat_id: str
    role: str
    content: str

class User(BaseModel):
    id: str
    name: str

class Chat(BaseModel):
    chat_id: str
    chat_name: str
    messages: list[Message]

class InvokeChatbotRequest(BaseModel):
    user_id: str
    chat_id: str
    user_message: str

class InvokeChatbotResponse(BaseModel):
    user_id: str
    chat_id: str
    llm_message: str

class AddUsersRequest(BaseModel):
    users: list[User]

class ChatsRequest(BaseModel):
    user_id: str

class ChatsResponse(BaseModel):
    chats: list[Chat]
