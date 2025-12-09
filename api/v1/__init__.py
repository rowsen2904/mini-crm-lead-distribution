from fastapi import APIRouter

from api.v1 import operators, sources, contacts, stats

api_router = APIRouter()
api_router.include_router(operators.router)
api_router.include_router(sources.router)
api_router.include_router(contacts.router)
api_router.include_router(stats.router)
