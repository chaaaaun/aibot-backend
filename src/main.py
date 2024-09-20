from fastapi import FastAPI
from .db import lifespan
from .models import api, db

app = FastAPI(lifespan=lifespan)

@app.post("/conversations")
async def create_conversation(conversation: api.CreateConversationRequest) -> api.CreateConversationResponse:
    convo = db.Conversation(name=conversation.name, params=conversation.params)
    await convo.insert()
    return api.CreateConversationResponse(id=convo.id.__str__())

@app.get("/conversations")
async def list_conversations() -> api.ListConversationsResponse:
    convos = await db.Conversation.find_all().to_list()
    convos_models = [api.ListConversationsItem(id=convo.id.__str__(), name=convo.name, params=convo.params, tokens=convo.tokens) for convo in convos]
    return api.ListConversationsResponse(conversations=convos_models)

@app.put("/conversations/{id}", status_code=201)
async def update_conversation(id: str, conversation: api.UpdateConversationRequest):
    convo = db.Conversation(id=id, name=conversation.name, params=conversation.params)
    await convo.save()

@app.get("/conversations/{id}")
async def read_conversation(id: int):
    return {"message": "Hello World"}

@app.delete("/conversations/{id}")
async def delete_conversation(id: int):
    return {"message": "Hello World"}

@app.post("/queries")
async def create_query():
    return {"message": "Hello World"}