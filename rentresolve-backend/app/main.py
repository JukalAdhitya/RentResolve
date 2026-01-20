from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- STARTING RENTRESOLVE BACKEND ---")
    await init_db()
    print("--- DATABASE CONNECTED ---")
    yield
    print("--- SHUTTING DOWN ---")

# import logfire
# logfire.configure()
# logfire.instrument_pydantic() # Instrument Pydantic models for PydanticAI

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="RentResolve API", lifespan=lifespan)

# Ensure static/uploads exists
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to RentResolve API"}

from app.routes import auth, issues, analyze, email, users
app.include_router(auth.router)
app.include_router(issues.router)
app.include_router(analyze.router)
app.include_router(email.router)
app.include_router(users.router)
