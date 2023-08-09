from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId

router = APIRouter()

client = MongoClient(
    'mongodb+srv://yash23malode:9dtb8MGh5aCZ5KHN@cluster.u0gqrzk.mongodb.net/')
db = client['prakat23']
report_collection = db['report_collection']
crawled_sites = db['crawled_sites']


@router.get('/')
async def getAllReports():
    reports = list(report_collection.find())
    combined_data = []

    for report in reports:
        url_id = report['url_id']
        url_data = crawled_sites.find_one({"_id": ObjectId(url_id)})

        if url_data:
            combined_entry = {
                '_id': str(report['_id']),
                'url_id': str(url_data['_id']),
                # 'report': report['report'] if not None else "",
                'user_id': report['user_id'],
                'url': url_data['url'],
                'title': url_data['title'],
                'status': report['report_generated'],
                'name': report['name']
            }
            if (report['report_generated'] == 2):
                combined_entry['report'] = report['report']

            combined_data.append(combined_entry)
    # print(reports)
    # url_ids = []

    # for report in reports:
    #     url_ids.append(report['url_id'])

    # print(url_ids)
    # pipeline = [
    #     {
    #         "$match": {
    #             "_id": {"$in": url_ids}
    #         }
    #     }
    # ]

    return combined_data
