import pytest
import os
import json
import asyncio
from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager
from openai import OpenAI

from src.main import app
from src.models import api
from src.models.db import Conversation

@asynccontextmanager
async def _lifespan(app: FastAPI):
    # Initialize test database before running any tests
    DB_URI = os.getenv("TEST_DB_URI")
    DB_NAME = os.getenv("TEST_DB_NAME")
    client = AsyncIOMotorClient(DB_URI)
    client.get_io_loop = asyncio.get_running_loop
    await init_beanie(database=client[DB_NAME], document_models=[Conversation])

    print("Initializing LLM client")
    API_KEY = os.getenv("API_KEY")
    llm_client = OpenAI(api_key=API_KEY)
    app.llm_client = llm_client

    yield
    client.drop_database(DB_NAME)
    client.close()

sample_conversation = {
    "name": "test conversation",
    "params": {}
}
sample_conversation_updated = {
    "name": "test conversation updated",
    "params": {
        "temperature": 0.5
    }
}
def sample_message(id: str):
    return {
        "convo_id": id,
        "role": "user",
        "content": "Hello, world!"
    }

# Override the app's lifespan context with the test lifespan context
app.router.lifespan_context = _lifespan

@pytest.mark.anyio
async def test_create_conversation():
    with TestClient(app) as client:
        response = client.post("/conversations", data=json.dumps(sample_conversation))
        body = response.json()
        assert response.status_code == 200
        assert "id" in body
        convo = await Conversation.get(body["id"])
        assert convo is not None

@pytest.mark.anyio
async def test_list_conversations():
    with TestClient(app) as client:
        ids = []
        for _ in range(3):
            response = client.post("/conversations", data=json.dumps(sample_conversation))
            body = response.json()
            assert response.status_code == 200
            assert "id" in body
            ids.append(body["id"])
        response = client.get("/conversations")
        assert response.status_code == 200
        convos = await Conversation.find_all().to_list()
        for id in ids:
            assert any(convo.id.__str__() == id for convo in convos)

@pytest.mark.anyio
async def test_get_conversation():
    with TestClient(app) as client:
        response = client.post("/conversations", data=json.dumps(sample_conversation))
        body = response.json()
        response = client.get(f"/conversations/{body['id']}")
        body = response.json()
        assert response.status_code == 200
        assert body["name"] == sample_conversation["name"]
        assert body["params"] == api.LLMParams().model_dump()

@pytest.mark.anyio
async def test_update_conversation():
    with TestClient(app) as client:
        response = client.post("/conversations", data=json.dumps(sample_conversation))
        body = response.json()
        id = body["id"]
        response = client.put(f"/conversations/{id}", data=json.dumps(sample_conversation_updated))
        assert response.status_code == 201
        convo = await Conversation.get(id)
        assert convo.name == sample_conversation_updated["name"]
        assert convo.params.temperature == sample_conversation_updated["params"]["temperature"]

@pytest.mark.anyio
async def test_delete_conversation():
    with TestClient(app) as client:
        response = client.post("/conversations", data=json.dumps(sample_conversation))
        body = response.json()
        id = body["id"]
        response = client.delete(f"/conversations/{id}")
        assert response.status_code == 200
        convo = await Conversation.get(id)
        assert convo is None

@pytest.mark.anyio
async def test_create_query():
    with TestClient(app) as client:
        response = client.post("/conversations", data=json.dumps(sample_conversation))
        body = response.json()
        id = body["id"]

        response = client.post("/queries", data=json.dumps(sample_message(id)))
        body = response.json()
        assert response.status_code == 201
        assert "content" in body