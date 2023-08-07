from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import crawl_manager, search, auth_route
from config.config import initiate_database

app = FastAPI()


@app.on_event("startup")
async def start_database():
    await initiate_database()


origins = [
    "http://localhost:1212"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=search.router, prefix='/search')
app.include_router(router=crawl_manager.router, prefix='/crawl_manager')
app.include_router(router=auth_route.router, prefix="")
