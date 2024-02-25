import datetime

from pydantic import UUID4, BaseModel


class FollowersSchema(BaseModel):
    id: UUID4
    follower_id: UUID4
    user_id: UUID4
    created_at: datetime.datetime
