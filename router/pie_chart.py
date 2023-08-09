import pickle
from fastapi import APIRouter, Query
from pymongo import MongoClient

router = APIRouter()

client = MongoClient(
    'mongodb+srv://yash23malode:9dtb8MGh5aCZ5KHN@cluster.u0gqrzk.mongodb.net/')
db = client['prakat23']
collection = db['ner_tags']

pipeline = [
         {
        "$unwind": "$ents"
    },
    {
        "$group": {
            "_id": "$ents.label",
            "count": { "$sum": 1 }
        }
    }
]


@router.get('/')
async def getPieChartData():
    # # # Open the file in binary write mode and pickle the data
    # with open('pie_chart.pickle', 'wb') as file:
    #     pickle.dump(results, file)

    # if unique_results:
    #     print(unique_results[0])
    with open('pie_chart.pickle', 'rb') as file:
        results = pickle.load(file)

    return results