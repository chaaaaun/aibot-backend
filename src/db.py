from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from contextlib import asynccontextmanager

from fastapi import FastAPI
import os
from .models.db import Conversation

# Manage the DB connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    DB_URI = os.getenv("DB_URI")
    client = AsyncIOMotorClient(DB_URI)
    app.db_client = client
    await init_beanie(database=client.db_name,
                        document_models=[Conversation])

    yield
    app.db_client.close()
