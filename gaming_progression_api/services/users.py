from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from gaming_progression_api.models.users import UserCreate
from gaming_progression_api.services.auth import AuthService
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class UsersService:
    async def add_user(self, uow: IUnitOfWork, user: UserCreate):
        user_dict = user.model_dump()
        user_dict['password'] = await AuthService.hash_password(user.password)
        async with uow:
            unique_username = await uow.users.find_one(username=user.username)
            if unique_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='A user with the same username already exists',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            unique_email = await uow.users.find_one(email=user.email)
            if unique_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='A user with this email already exists',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def get_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    async def get_user(self, uow: IUnitOfWork, username: str):
        async with uow:
            users = await uow.users.find_one(username=username)
            return users

    async def authenticate_user(self, uow: IUnitOfWork, username: str, password: str):
        async with uow:
            user = await uow.users.find_one(username=username)
        if not user:
            return False
        if not await AuthService.verify_password(password, user.password):
            return False
        return user
