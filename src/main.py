from fastapi import FastAPI
from .lifecycle import lifespan
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
async def read_conversation(id: str) -> api.ReadConversationResponse:
    convo = await db.Conversation.get(id)
    msgs = [api.ReadConversationQueryItem(role=msg.role, content=msg.content) for msg in convo.messages]
    return api.ReadConversationResponse(id=convo.id.__str__(), name=convo.name, params=convo.params, tokens=convo.tokens, messages=msgs)

@app.delete("/conversations/{id}")
async def delete_conversation(id: str):
    convo = await db.Conversation.get(id)
    await convo.delete()

@app.post("/queries", status_code=201)
async def create_query(query: api.CreateQueryRequest) -> api.CreateQueryResponse:
    convo = await db.Conversation.get(query.convo_id)
    msgs = convo.messages + [db.Message(role=query.role, content=query.content)]
    try:
        completion = app.llm_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[msg.model_dump() for msg in msgs],
        )
        answer = completion.choices[0].message
        resp = db.Message(role=answer.role, content=answer.content)
        convo.messages = msgs + [resp]
        convo.tokens += completion.usage.total_tokens
        await convo.save()
        return api.CreateQueryResponse(role=answer.role, content=answer.content)
    except Exception as e:
        return api.ApiErrorResponse(code=422, message=str(e))