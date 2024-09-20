from datetime import datetime
from pydantic import Field
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

class AuditMessage(Document):
    event: str
    timestamp: datetime = Field(default_factory=datetime.now)
    convo_id: str
    message: str

    class Settings:
        name = "audit"
        indexes = [
            "id"
        ]