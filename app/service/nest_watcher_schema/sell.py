from sqlalchemy import Column, String, INTEGER, DateTime

from app.service.common_schema.database import FajneBase


class Sell(FajneBase):
    __tablename__ = 'sell'

    suggestion_id = Column('suggestion_id', String, primary_key=True)
    sell_id = Column('sell_id', String)
    device_id = Column('device_id', String)
    sold_assorment = Column('sold_assortment', String)

    neural_duration = Column('neural_duration', INTEGER)
    transaction_duration = Column('transaction_duration', INTEGER)
    transaction_timestamp = Column('transaction_timestamp', DateTime)

    def json(self):
        content = {
            'suggestion_id': self.suggestion_id,
            'sold_assortment': self.sold_assorment,
            "pos1": self.pos1,
        }
        return content

    def __repr__(self):
        return (f"<Sell suggestion_id={self.suggestion_id}, "
                f"sell_id={self.sell_id}, "
                f"device_id={self.device_id} "
                f"sold_assorment={self.sold_assorment}, "
                f"neural_duration={self.neural_duration}"
                f"transaction_duration={self.transaction_duration}"
                f"transaction_timestamp={self.transaction_timestamp}"
                )


def map_sell_data_to_dto(json_data):
    sell = Sell(
        suggestion_id=json_data['suggestion_id'],
        sell_id=json_data['sell_id'],
        device_id=json_data['device_id'],
        sold_assorment=json_data['sold_assortment'],
        neural_duration=json_data['neural_duration'],
        transaction_duration=json_data['transaction_duration'],
        transaction_timestamp=json_data['transaction_timestamp']
    )

    return sell
