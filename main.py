from fastapi import FastAPI

from api.v1 import api_router
from core.db import Base, engine

# Create tables on startup for demo purposes
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini CRM lead distribution")

app.include_router(api_router, prefix="/api/v1")
