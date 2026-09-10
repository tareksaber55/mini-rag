from fastapi import FastAPI
from routes import base,data
from pymongo import AsyncMongoClient
from helpers.config import get_settings


app = FastAPI()


@app.on_event('startup')
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncMongoClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MOGODB_DATABASE]

@app.on_event('shutdown')
async def shutdown_db_client():
    app.mongo_conn.close()

app.include_router(base.base_router)
app.include_router(data.data_router)