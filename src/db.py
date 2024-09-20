import asyncio
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
    print("Initializing DB connection")
    DB_URI = os.getenv("DB_URI")
    DB_NAME = os.getenv("DB_NAME")

    client = AsyncIOMotorClient(DB_URI)
    client.get_io_loop = asyncio.get_running_loop
    app.db_client = client
    await init_beanie(database=client[DB_NAME], document_models=[Conversation])
    yield
    app.db_client.close()
