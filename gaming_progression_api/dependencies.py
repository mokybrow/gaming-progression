from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from gaming_progression_api.models.users import BaseUser
from gaming_progression_api.services.auth import AuthService
from gaming_progression_api.services.unitofwork import IUnitOfWork, UnitOfWork
from gaming_progression_api.settings import get_settings

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

settings = get_settings()

access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(uow: UOWDep, token: Annotated[str, Depends(oauth2_scheme)]):
    return await AuthService().get_current_user(uow, token)


async def get_current_active_user(current_user: Annotated[BaseUser, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
