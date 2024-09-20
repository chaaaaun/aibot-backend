import asyncio
import os
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from contextlib import asynccontextmanager
from openai import OpenAI
from fastapi import FastAPI
from .models.db import Conversation, AuditMessage

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing DB connection")
    DB_URI = os.getenv("DB_URI")
    DB_NAME = os.getenv("DB_NAME")

    client = AsyncIOMotorClient(DB_URI)
    client.get_io_loop = asyncio.get_running_loop
    app.db_client = client
    await init_beanie(database=client[DB_NAME], document_models=[Conversation, AuditMessage])

    print("Initializing LLM client")
    API_KEY = os.getenv("API_KEY")
    client = OpenAI(api_key=API_KEY)
    app.llm_client = client
    
    yield
    app.db_client.close()
