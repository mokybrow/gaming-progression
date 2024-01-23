from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from gaming_progression_api.dependencies import UOWDep, access_token_expires, get_current_user
from gaming_progression_api.models.tokens import Token
from gaming_progression_api.models.users import BaseUser, UserCreate
from gaming_progression_api.services.auth import AuthService
from gaming_progression_api.services.users import UsersService
from gaming_progression_api.settings import get_settings

settings = get_settings()


router = APIRouter(
    tags=['auth'],
)


@router.post('/token')
async def login_for_access_token(uow: UOWDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await UsersService().authenticate_user(uow, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = await AuthService().create_access_token({'sub': user.username}, access_token_expires)
    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me/', response_model=BaseUser)
async def read_users_me(current_user: Annotated[BaseUser, Depends(get_current_user)]):
    return current_user


@router.post('/sign-up')
async def add_user(user: UserCreate, uow: UOWDep):
    user_id = await UsersService().add_user(uow, user)

    return {'user_id': user_id}
