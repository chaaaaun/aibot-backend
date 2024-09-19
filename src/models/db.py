import pymongo
from pydantic import BaseModel
from beanie import Document
from .api import LLMParams


class Messages(BaseModel):
    role: str
    content: str

class Conversation(Document):  # This is the model
    name: str
    params: LLMParams
    tokens: int
    messages: list[Messages]

    class Settings:
        name = "conversations"
        indexes = [
            "id"
        ]