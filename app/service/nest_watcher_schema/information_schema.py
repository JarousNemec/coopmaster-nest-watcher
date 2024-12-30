from sqlalchemy import Column, Integer, Double

from app.service.common_schema.database import FajneBase


class InformationSchema(FajneBase):
    __tablename__ = 'information_schema'

    schema_version = Column("schema_version", Integer, primary_key=True)
    creation_time = Column("creation_time", Double)

    def __repr__(self):
        return f"<InformationSchema schema_version={self.schema_version}, creation_time={self.creation_time}>"