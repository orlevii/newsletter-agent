from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    url: str
    created_at: datetime | None = None
    title: str | None = None
    summary: str | None = None
