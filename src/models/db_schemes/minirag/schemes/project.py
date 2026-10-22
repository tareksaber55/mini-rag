from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column,Integer,DateTime,func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
class Project(SQLAlchemyBase):

    __tablename__ = 'projects'

    project_id = Column(Integer,primary_key=True,autoincrement=True)
    '''
    Important: Pass uuid.uuid4, not uuid.uuid4(). The first passes a callable that generates a new UUID for each insert; 
    the second generates one UUID immediately when the model is defined.
    '''
    project_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)

    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    '''
    Use default when SQLAlchemy/Python should generate the value, and server_default when the database should generate it.
    '''
    updated_at = Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)
    '''
    Date	                2026-10-10	                Calendar date only
    DateTime	            2026-10-10 14:30:25	        Date and time
    DateTime(timezone=True)	2026-10-10 11:30:25+00:00	Date and time with timezone semantics
    '''
    assets = relationship("Asset", back_populates="project")
    chunks = relationship("DataChunk", back_populates="project")