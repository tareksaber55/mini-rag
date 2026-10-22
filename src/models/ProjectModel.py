import math
from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy import select,func
class ProjectModel(BaseDataModel):
    def __init__(self, db_client:object):
        super().__init__(db_client=db_client)
        self.collection = db_client

    @classmethod
    async def create_instance(cls,db_client:object):
        instance = cls(db_client)
        return instance
    


    async def create_project(self,project:Project):
        async with self.db_client() as session:
            async with session.begin():
                # 1. No 'await' here — session.add() is synchronous
                session.add(project)
                '''
                When Python exits the async with session.begin(): block, 
                SQLAlchemy automatically runs await session.commit() for you.
                '''
            await session.refresh(project)
        return project

    async def get_or_create_project(self,project_id:int):
        async with self.db_client() as session:
             async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project_record = result.scalar_one_or_none()
        if project_record is None:
            project = Project(
                project_id = project_id
            )
            project_record = await self.create_project(project=project)
        return project_record



    async def get_all_projects(self,page: int = 1,page_size: int = 10):
        if page < 1:
            raise ValueError("page must be greater than or equal to 1")
        if page_size < 1:
            raise ValueError("page_size must be greater than or equal to 1")
        async with self.db_client() as session:
            async with session.begin():
                skip = (page - 1)*page_size
                query = select(Project).offset(skip).limit(page_size)
                projects = await session.execute(query).scalars().all()
                return projects

    
        


