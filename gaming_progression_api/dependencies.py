from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from gaming_progression_api.models.service import ServiceResponseModel
from gaming_progression_api.models.users import User, UserSchema
from gaming_progression_api.services.auth import AuthService
from gaming_progression_api.services.unitofwork import IUnitOfWork, UnitOfWork
from gaming_progression_api.settings import get_settings

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


settings = get_settings()

access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
verify_token_expires = timedelta(minutes=settings.verify_token_expire_minutes)
reset_token_expires = timedelta(minutes=settings.reset_token_expire_minutes)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/sign-in')


async def get_current_user(
    uow: UOWDep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    return await AuthService().get_current_user(uow, token)


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.user_roles.is_verified:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


async def get_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.user_roles.is_superuser:
        raise HTTPException(status_code=400, detail='Youre not superuser')
    return current_user
