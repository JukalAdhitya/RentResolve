import asyncio
import os
from dotenv import load_dotenv

# Load .env explicitly to handle different running directories
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.db.models import User, Issue
from app.core.config import settings
from textwrap import dedent

async def check_db():
    print("Connecting to database...")
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database=client.get_default_database(), document_models=[User, Issue])
    
    print("\n--- USERS ---")
    users = await User.find_all().to_list()
    if not users:
        print("No users found.")
    for user in users:
        print(dedent(f"""
        ID: {user.id}
        Email: {user.email}
        Role: {user.role}
        Created At: {user.created_at}
        --------------------------------
        """).strip())

    print("\n\n--- ISSUES ---")
    issues = await Issue.find_all().to_list()
    if not issues:
        print("No issues found.")
    for issue in issues:
        print(dedent(f"""
        ID: {issue.id}
        Title: {issue.title}
        Tenant ID: {issue.tenant_id}
        Status: {issue.status}
        Created At: {issue.created_at}
        --------------------------------
        """).strip())

if __name__ == "__main__":
    asyncio.run(check_db())
