import uuid

from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from gaming_progression_api.integrations.database import Base
from gaming_progression_api.models.users import User, UserCreate, UserSchema


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
            disabled=self.disabled,
        )
