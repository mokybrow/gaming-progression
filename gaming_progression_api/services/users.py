from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4

from gaming_progression_api.models.users import PatchUser, UserCreate
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
                )
            unique_email = await uow.users.find_one(email=user.email)
            if unique_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='A user with this email already exists',
                )
            await uow.users.add_one(user_dict)
            await uow.commit()
            raise HTTPException(
                status_code=status.HTTP_201_CREATED,
                detail='User has been successfully created',
            )

    async def get_user_profile(self, uow: IUnitOfWork, username: str):
        async with uow:
            user = await uow.users.find_one_user(username=username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found',
            )
        return user

    async def get_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    async def get_user(self, uow: IUnitOfWork, email: str):
        async with uow:
            user = await uow.users.find_one(email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exist",
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return user

    async def get_user_for_verify(self, uow: IUnitOfWork, email: str):
        async with uow:
            user = await uow.users.find_one(email=email)
            if not user.is_verified:
                return user
            return False

    async def authenticate_user(self, uow: IUnitOfWork, username: str, password: str):
        async with uow:
            user = await uow.users.find_one(username=username)
        if not user:
            return False
        if not await AuthService.verify_password(plain_password=password, hashed_password=user.password):
            return False
        return user

    async def patch_user(self, uow: IUnitOfWork, user_id: UUID4, user: PatchUser):
        user_dict = user.model_dump()
        async with uow:
            try:
                user_data = await uow.users.find_one(id=user_id)
                if user_data.email != user_dict['email']:
                    await uow.users.edit_one(data={'is_verified': False}, id=user_id)
                user_dict['password'] = await AuthService.hash_password(user_dict['password'])
                await uow.users.edit_one(data=user_dict, id=user_id)
                await uow.commit()
                return True
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='An error occurred while changing data',
                    headers={'WWW-Authenticate': 'Bearer'},
                )

    async def follow_on_user(
        self,
        uow: IUnitOfWork,
        follower_id: UUID4,
        user_id: UUID4,
    ):
        async with uow:
            find_pair = await uow.followers.find_one(user_id=user_id, follower_id=follower_id)
            if find_pair:
                await uow.followers.delete_one(user_id=user_id, follower_id=follower_id)
                await uow.commit()
                return f"Successfully unfollow on user {user_id}"
            await uow.followers.add_one(data={"follower_id": follower_id, "user_id": user_id})
            await uow.commit()
            return f'Successfully follow on user {user_id}'
