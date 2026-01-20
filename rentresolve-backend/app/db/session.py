from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import User, Issue
import os

async def init_db():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL", "mongodb://localhost:27017/rentresolve"))
    await init_beanie(database=client.rentresolve, document_models=[User, Issue])
