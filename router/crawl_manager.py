from fastapi import APIRouter, HTTPException, Body
from rabbitmq.RabbitMq import RabbitMQ
from model.DTO.custom_crawler_model import StartCrawlRequestBody, StopCrawlRequestBody
from models.CrawlerInstance import crawlerinstance
from crud.crawler_instance_crud import add_crawler_instance, reterieve_all_crawler_instance

router = APIRouter()

COMMAND_CREATE_CRAWLER = 'create_crawler'
COMMAND_STOP_CRAWLER = 'stop_crawler'
COMMAND_STATUS_CRAWLER = 'status_crawler'
COMMAND_TERMINATE_CRAWLER = 'terminate_crawler'


@router.get('/')
async def get_all_crawl():
    crawlers = await reterieve_all_crawler_instance()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Crawlers fetched Successfully",
        "data": crawlers
    }


@router.post('/start')
async def custom_crawl_start(body: StartCrawlRequestBody = Body()):
    print(body)
    crawler_exists = await crawlerinstance.find_one(body.url == crawlerinstance.url)
    if crawler_exists:
        raise HTTPException(
            status_code=409, detail="You have already crawled that url")

    crawler_body = crawlerinstance(
        limit=body.limit, url=body.url, same_domain=body.same_domain, userId='22', status=0)

    crawler = await add_crawler_instance(crawler_body)
    rabbitmq = RabbitMQ()
    print(crawler.id)
    rabbitmq.publish_to_queue(
        {"command": COMMAND_CREATE_CRAWLER, "crawlerId": str(crawler.id)})
    return 'Queued your crawler', crawler


@router.post("/stop")
async def custom_crawl_stop(body: StopCrawlRequestBody = Body()):
    try:
        crawler = await crawlerinstance.get(body.crawlerId)
        if crawler is None:
            raise HTTPException(
                status_code=404, detail="Crawler does not exist"
            )
        crawler.status = 3
        await crawler.save()

        rabbitmq = RabbitMQ()
        rabbitmq.publish_to_queue(
            {"command": COMMAND_STOP_CRAWLER, "crawlerId": str(crawler.id)})

        return crawler
    except Exception as e:
        raise HTTPException(400, detail=str(e))
