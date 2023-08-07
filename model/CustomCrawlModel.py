from pydantic import BaseModel, Field
from database.db import PyObjectId
from bson import ObjectId


# def crawler_serializer(crawler) -> dict:
#     return {
#         'id': str(crawler['_id']),
#         'url': crawler["url"],
#         "same_domain": crawler["same_domain"],
#         "limit": crawler["limit"],
#         "crawlerId": crawler["crawlerId"],
#         "command": crawler["command"]
#     }


# def crawlers_serializer(crawlers) -> list:
#     return [crawler_serializer(crawler) for crawler in crawlers]
def crawler_serializer(crawl):
    print("inside crawler serializer")
    print(crawl)
    return CustomCrawlModel(url=crawl['url'], status=0, userid=str(crawl['userId']), limit=1000, same_domain=crawl['same_domain'], )


def crawlers_serializer(crawlers):
    return [crawler_serializer(crawler) for crawler in crawlers]


class CustomCrawlModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    # userid: str = Field()
    userid: str = Field()
    url: str = Field()
    limit: int = Field()
    same_domain: bool | None = Field()
    status: int = Field()

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "userid": "User mongo object id",
                "url": "abc.onion",
                "limit": 100,
                "same_domain": True,
                "status": 0
            }
        }


# class UpdateStudentModel(BaseModel):
#     status: int
#     # email: Optional[str]
#     # course: Optional[str]
#     # gpa: Optional[float]

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "status": 2,
#             }
#         }
