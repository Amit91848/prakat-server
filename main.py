from config.config import initiate_database
from router import crawl_manager, search, auth_route, btc_address, report_route, data_breach
from router import crawl_manager, search, auth_route, btc_address, report_route, pie_chart, tor_stats, mail_route
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(router=btc_address.router, prefix="/btc_address")
app.include_router(router=report_route.router, prefix="/report")
app.include_router(router=pie_chart.router, prefix="/pie_chart")
app.include_router(router=tor_stats.router, prefix="/tor_stats")
app.include_router(router=mail_route.router, prefix="/mail")
app.include_router(router=data_breach.router, prefix="/data_breach")
app.include_router(router=auth_route.router, prefix="")
