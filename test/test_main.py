import pytest
import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient

from src.main import app
from src.models.db import Conversation
from src.models.api import LLMParams, CreateConversationRequest, UpdateConversationRequest, CreateQueryRequest

async def _lifespan():
    # Initialize test database before running any tests
    DB_URI = os.getenv("TEST_DB_URI")
    DB_NAME = os.getenv("TEST_DB_NAME")
    client = AsyncIOMotorClient(DB_URI)
    await init_beanie(database=client[DB_NAME], document_models=[Conversation])
    yield

app.router.lifespan_context = _lifespan
client = TestClient(app)

sample_conversation = CreateConversationRequest(name="test conversation", params=LLMParams())
sample_conversation_updated = UpdateConversationRequest(name="test conversation_updated", params=LLMParams(temperature=0.5))
sample_message = CreateQueryRequest(role="user", content="Hello")

@pytest.mark.anyio
async def test_create_conversation():
    response = client.post("/conversations", content=sample_conversation)
    body = response.json()
    assert response.status_code == 201
    assert "id" in body
    convo = await Conversation.find_one(body["id"])
    assert convo is not None

@pytest.mark.anyio
async def test_list_conversations():
    ids = []
    for _ in range(3):
        response = client.post("/conversations", content=sample_conversation)
        body = response.json()
        assert response.status_code == 200
        assert "id" in body
        ids.append(body["id"])
    response = client.get("/conversations")
    assert response.status_code == 200
    convos = await Conversation.find_all().to_list()
    for id in ids:
        assert any(convo.id == id for convo in convos)

@pytest.mark.anyio
async def test_get_conversation():
    response = client.post("/conversations", content=sample_conversation)
    body = response.json()
    assert response.status_code == 200
    assert body["name"] == sample_conversation.name
    assert body["params"] == sample_conversation.params.model_dump()

@pytest.mark.anyio
async def test_update_conversation():
    response = client.post("/conversations", content=sample_conversation)
    body = response.json()
    id = body["id"]
    response = client.put(f"/conversations/{id}", sample_conversation_updated)
    assert response.status_code == 201
    convo = await Conversation.find_one(id)
    assert convo.name == sample_conversation_updated.name
    assert convo.params.temperature == sample_conversation_updated.params.temperature

@pytest.mark.anyio
async def test_delete_conversation():
    response = client.post("/conversations", content=sample_conversation)
    body = response.json()
    id = body["id"]
    response = client.delete(f"/conversations/{id}")
    assert response.status_code == 200
    convo = await Conversation.find_one(id)
    assert convo is None

@pytest.mark.anyio
async def test_create_query():
    response = client.post("/queries", content=sample_message)
    body = response.json()
    assert response.status_code == 201
    assert "id" in body