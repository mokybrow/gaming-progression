


import datetime
from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict


class Games(BaseModel):
    id: UUID4
    title: str
    cover: Optional[str]
    description: Optional[str]
    slug: str
    release_date: Optional[datetime.datetime]
    playtime: Optional[int]
    completed_count: Optional[int]
    wishlist_count: Optional[int] 
    favorite_count : Optional[int]
    avg_rate : Optional[float]

    model_config = ConfigDict(arbitrary_types_allowed=True)
