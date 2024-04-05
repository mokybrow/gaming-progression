from fastapi import APIRouter

from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/feeds',
    tags=['feeds'],
)
