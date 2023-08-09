import requests
import json
from fastapi import APIRouter, Query

url = "https://breachdirectory.p.rapidapi.com/"


router = APIRouter()


@router.get('/')
async def get_breach_status(email: str = Query()):
    querystring = {"func": "auto", "term": f"{email}"}

    # headers = {
    #     "X-RapidAPI-Key": "b5b244a76fmshe0f84fb7bf6463fp18326ejsn09a683d93902",
    #     "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
    # }
    headers = {'X-RapidAPI-Key': '755f30fc3emsh8ed8af88f73ce9dp10059ajsn1b20dec94ffe',
               'X-RapidAPI-Host': 'breachdirectory.p.rapidapi.com'}
    response = requests.get(url, headers=headers, params=querystring)
    resp_json = json.loads(response.text)
    sources = []
    for result in resp_json["result"]:
        source = result["sources"][0]
        print(source)
        if source != 'Unknown':
            sources.append(source)
    return sources
