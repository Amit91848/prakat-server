from pydantic import BaseModel
from bson import ObjectId


class StartCrawlRequestBody(BaseModel):
    url: str
    userId: int  = 22
    same_domain: bool  = True
    limit: int  = 1000


class StopCrawlRequestBody(BaseModel):
    crawlerId: str
