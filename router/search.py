from fastapi import APIRouter, HTTPException, Query
from typing import List
from model.DTO.search_result import SearchResult
from service.search_services import load_and_vectorize_data, rank_documents
from pathlib import Path
from models.CrawledSites import crawled_sites
from pymongo import MongoClient
from typing import Annotated

router = APIRouter()

# data_path = Path(__file__).parent.parent /"data"/"cleaned_data.json"
client = MongoClient(
    'mongodb+srv://yash23malode:9dtb8MGh5aCZ5KHN@cluster.u0gqrzk.mongodb.net/')
db = client['prakat23']
crawled_sites = db['crawled_sites']

collection = crawled_sites.find().limit(800)

# collection = await crawled_sites.find_all().to_di()
# collection = crawled_sites.find()
df, vectorizer, vector_tfidf = load_and_vectorize_data(collection)

# pipeline = [
#     {"$unwind": "$tags"},
#     {"$group": {"_id": None, "unique_tags": {"$addToSet": "$tags"}}}
# ]
# result = crawled_sites.aggregate(pipeline)

# unique_tags = result.next()["unique_tags"]
# print(unique_tags)

# @router.get("/", response_model=List[SearchResult])

unique_tags = ['Heroin', 'Stimulants', 'Revolvers', 'Marijuana', 'Phone Number', 'Barbiturates', 'Steroids', 'BTC Wallet Address', 'Depressants ', 'Bath Salts', 'Fentanyl', 'Machine Guns', 'Pistol', 'Monero Wallet Address', 'DXM', 'Assault Rifle',
               'Rifles', 'Hallucinogens', 'Hydromorphone', 'Shotguns', 'Ecstasy', 'Salvia Divinorum', 'Opiods', 'Oxycodone', 'Cocaine', 'Metamphetamine', 'Sniper Rifle', 'Spice/ K2, Synthetic Marijuana', 'Rohypnol', 'SubMachine Gun', 'Amphetamines', 'Benzodiazepines']


@router.get("/")
async def search(q: Annotated[str | None, Query(min_length=1)] = None, page: int = Query(1, gt=0), pageCount: int = Query(20, ge=1), tags: Annotated[str | None, Query()] = None):
    # print(q)
    if q:
        try:
            results = rank_documents(
                q, vectorizer, vector_tfidf, df, page, pageCount, tags)
            # return await crawled_sites.find_all().limit(100).to_list()
            return results
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))
    else:
        return []
