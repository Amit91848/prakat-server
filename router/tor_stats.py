import requests
import csv
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response

router = APIRouter()

def get_processed_data(csv_data:str):
    processed_data = []
    lines = csv_data.strip().split('\n')
    reader = csv.reader(lines[5:], delimiter=',')
    
    headers = None
    for i, row in enumerate(reader):
        if i == 0:
            headers = row
        else:
            data_point = {
                'date': row[0],
                'users': int(row[2]),
            }
            processed_data.append(data_point)
    
    return processed_data

@router.get('/')
async def getAllTorStats(
    start: str = Query(),
    end: str = Query(),
    country: str = Query()
    ):
    try:
        url = f"https://metrics.torproject.org/userstats-relay-country.csv?start={start}&end={end}&country={country}&events=off"
        response = requests.get(url)

        if response.status_code == 200:
            content = response.text
            processed_data = get_processed_data(content)
            return processed_data
        else:
            return JSONResponse(content={"error": "Failed to fetch Tor metrics"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

