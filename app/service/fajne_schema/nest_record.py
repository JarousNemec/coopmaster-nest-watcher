from sqlalchemy import Column, String, INTEGER, DateTime, Integer

from app.service.common_schema.database import FajneBase


class NestRecord(FajneBase):
    __tablename__ = 'nest_record'

    id = Column(Integer, primary_key=True)
    nest_id = Column('nest_id', String)
    weight = Column('weight', INTEGER)
    timestamp = Column('timestamp', String)

    def json(self):
        content = {
            'nest_id': self.nest_id,
            'weight': self.weight,
            "timestamp": self.timestamp,
        }
        return content

    def __repr__(self):
        return (f"<NestRecord nest_id={self.nest_id}, "
                f"weight={self.weight}, "
                f"timestamp={self.timestamp} "
                )

def map_nestInfo_data_to_dto(json_data):
    record = NestRecord(
        nest_id=json_data['nest_id'],
        weight=json_data['weight'],
        timestamp=json_data['timestamp']
    )

    return record
