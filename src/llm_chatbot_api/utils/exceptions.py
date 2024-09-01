from fastapi import HTTPException

class UserDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User with the given id does not exist")

class ChatDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Chat with the given id does not exist")

class MessageIsEmpty(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Message is empty")

class MessageIsTooLong(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Message is too long")