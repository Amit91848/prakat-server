from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from models.CrawlerInstance import crawlerinstance
from models.Admin import Admin
from models.CrawledSites import crawled_sites


async def initiate_database():
    client = AsyncIOMotorClient(
        "mongodb+srv://yash23malode:9dtb8MGh5aCZ5KHN@cluster.u0gqrzk.mongodb.net/")
    await init_beanie(database=client.prakat23, document_models=[crawlerinstance, Admin, crawled_sites])
