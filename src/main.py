from fastapi import FastAPI
from .db import lifespan
from .models.api import CreateConversationRequest, CreateConversationResponse
from .models.db import Conversation

app = FastAPI(lifespan=lifespan)

@app.post("/conversations")
async def create_conversation(conversation: CreateConversationRequest) -> CreateConversationResponse:
    convo = Conversation(name=conversation.name, params=conversation.params)
    await convo.insert()
    return CreateConversationResponse(id=convo.id.__str__())

@app.get("/conversations")
async def list_conversations():
    return {"message": "Hello World"}

@app.put("/conversations/{id}")
async def update_conversation(id: int):
    return {"message": "Hello World"}

@app.get("/conversations/{id}")
async def read_conversation(id: int):
    return {"message": "Hello World"}

@app.delete("/conversations/{id}")
async def delete_conversation(id: int):
    return {"message": "Hello World"}

@app.post("/queries")
async def create_query():
    return {"message": "Hello World"}