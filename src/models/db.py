import pymongo
from pydantic import BaseModel
from beanie import Document
from .api import LLMParams, Message

class Conversation(Document):  # This is the model
    name: str
    params: LLMParams
    tokens: int = 0
    messages: list[Message] = []

    class Settings:
        name = "conversations"
        indexes = [
            "id"
        ]