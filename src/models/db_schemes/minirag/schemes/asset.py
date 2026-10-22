from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column,Integer,String,DateTime,func,JSON,ForeignKey,Index
from sqlalchemy.dialects.postgresql import UUID,JSONB
import uuid
from models.enums import AssetTypeEnum
from sqlalchemy.orm import relationship

class Asset(SQLAlchemyBase):
    __tablename__ = 'assets'
    asset_id = Column(Integer,autoincrement=True,primary_key=True)
    asset_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)
    asset_project_id = Column(Integer,ForeignKey("projects.project_id"),nullable=False)
    asset_type = Column(String,default=AssetTypeEnum.FILE.value,nullable=False)
    asset_name = Column(String,nullable=False)
    asset_size = Column(Integer,nullable=False)
    asset_config = Column(JSONB,nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    project = relationship('Project',back_populates='assets')
    chunks = relationship("DataChunk", back_populates="asset")
    __table_args__ = (
        Index('ix_asset_project_id',asset_project_id),
        Index('ix_asset_type',asset_type)
    )
    
