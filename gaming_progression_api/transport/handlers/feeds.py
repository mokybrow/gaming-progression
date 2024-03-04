from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from gaming_progression_api.dependencies import UOWDep, get_current_active_user
from gaming_progression_api.models.playlists import AddPlaylist, PlaylistResponseModel
from gaming_progression_api.models.users import User
from gaming_progression_api.services.playlists import PlaylistsService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    prefix='/feeds',
    tags=['feeds'],
)
