from fastapi import FastAPI
from routes import base,data,nlp
from contextlib import asynccontextmanager
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    postgres_conn = f'postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}'
    # Manages database connectivity and connections
    app.db_engine = create_async_engine(postgres_conn)
    # Provides an interface to interact with the database
    app.db_client = sessionmaker(app.db_engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False
                                )
    

    # LLM Provider Factory
    llm_provider_factory = LLMProviderFactory(
        config=settings
    )

    # Generation client
    app.generation_client = llm_provider_factory.create(
        provider=settings.GENERATION_BACKEND
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

    app.vectordb_client = VectorDBProviderFactory(settings).create(
        provider=settings.VECTOR_DB_BACKEND
    )
    app.vectordb_client.connect()

    app.template_parser = TemplateParser(default_language=settings.DEFAULT_LANGUAGE)
    yield

    # Shutdown
    await app.db_engine.dispose()
    app.vectordb_client.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)