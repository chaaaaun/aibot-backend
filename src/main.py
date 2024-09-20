from fastapi import FastAPI
from .db import lifespan
from .models.api import CreateConversationRequest, CreateConversationResponse, ListConversationsItem, ListConversationsResponse
from .models.db import Conversation

app = FastAPI(lifespan=lifespan)

@app.post("/conversations")
async def create_conversation(conversation: CreateConversationRequest) -> CreateConversationResponse:
    convo = Conversation(name=conversation.name, params=conversation.params)
    await convo.insert()
    return CreateConversationResponse(id=convo.id.__str__())

@app.get("/conversations")
async def list_conversations() -> ListConversationsResponse:
    convos = await Conversation.find_all().to_list()
    convos_models = [ListConversationsItem(id=convo.id.__str__(), name=convo.name, params=convo.params, tokens=convo.tokens) for convo in convos]
    return ListConversationsResponse(conversations=convos_models)

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