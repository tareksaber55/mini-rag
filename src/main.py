from fastapi import FastAPI
from routes import base,data
from pymongo import AsyncMongoClient
from contextlib import asynccontextmanager
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    # MongoDB
    app.mongo_conn = AsyncMongoClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MOGODB_DATABASE]

    # LLM Provider Factory
    llm_provider_factory = LLMProviderFactory(
        config=settings.model_dump()
    )

    # Generation client
    app.generation_client = llm_provider_factory.create(
        settings.GENERATION_BACKEND
    )
    app.generation_client.set_generation_model(
        settings.GENERATION_MODEL_ID
    )

    # Embedding client
    app.embedding_client = llm_provider_factory.create(
        settings.EMBEDDING_BACKEND
    )
    app.embedding_client.set_embedding_model(
        settings.EMBEDDING_MODEL_ID,
        settings.EMBEDDING_MODEL_SIZE
    )

    yield

    # Shutdown
    await app.mongo_conn.close()


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)