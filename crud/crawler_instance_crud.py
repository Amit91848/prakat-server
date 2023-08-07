from beanie import PydanticObjectId
from typing import List

from models.CrawlerInstance import crawlerinstance

crawler_collection = crawlerinstance


async def add_crawler_instance(new_crawler: crawlerinstance) -> crawlerinstance:
    crawler = await new_crawler.create()
    return crawler


async def reterieve_all_crawler_instance() -> List[crawlerinstance]:
    crawlers = await crawler_collection.all().to_list()

    return crawlers
