from pydantic import BaseModel
from bson import ObjectId


class StartCrawlRequestBody(BaseModel):
    url: str
    userId: int | None = 22
    same_domain: bool | None = True
    limit: int | None = 1000


class StopCrawlRequestBody(BaseModel):
    crawlerId: str
