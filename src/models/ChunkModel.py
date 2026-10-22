from bson.objectid import ObjectId
from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne
import math
from sqlalchemy import select,func,delete

class ChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = db_client


    @classmethod
    async def create_instance(cls,db_client:object):
        instance = cls(db_client)
        return instance
    

    
    async def insert_chunk(self,chunk: DataChunk):
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.refresh(chunk)
        return chunk
            

    async def get_chunk(self,chunk_id:str):
        async with self.db_client() as session:
            async with session.begin():
                query = select(DataChunk).where(DataChunk.chunk_id == chunk_id)
                result = await session.execute(query)
                chunk = result.scalar_one_or_none()
        return chunk

    async def insert_many_chunks(self,chunks:list,batch_size=100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0,len(chunks),batch_size): 
                    batch = chunks[i:i+batch_size]
                    session.add_all(batch)
                    await session.flush()
        return len(chunks)
        


    async def delete_chunks_by_project_id(self,project_id:int):
        async with self.db_client() as session:
            async with session.begin():
                query = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
                result = await session.execute(query)
        return result.row_count
        

    async def get_project_chunks(self,project_id:int,
                                 page:int = 1 , page_size:int = 100):
        if page < 1 :
            raise ValueError("page must be greater than or equal to 1")
        if page_size < 1:
            raise ValueError("page_size must be greater than or equal to 1")
        async with self.db_client() as session:
            async with session.begin():
                skip = (page - 1)*page_size
                query = select(DataChunk).where(DataChunk.chunk_project_id == project_id).offset(skip).limit(page_size)
                result = await session.execute(query)
                chunks = result.scalars().all()
        return chunks
