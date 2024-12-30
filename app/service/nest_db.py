import logging
import random
import time
from datetime import datetime, timedelta

from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.orm import sessionmaker

from app.service.fajne_schema.fajne_schema_creator import CoopMasterDBCreator
from app.service.fajne_schema.information_schema import InformationSchema
from app.service.fajne_schema.nest_record import NestRecord, map_nestInfo_data_to_dto
from app.service.fajne_schema.sell import Sell


class NestSellDB:

    def __init__(self, host, port, database, user, password):
        try:
            conn_string = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}'
            engine = create_engine(conn_string)
            self.engine = engine
            session = sessionmaker(bind=engine)
            self.session = session()
        except Exception as e:
            logging.error(f"Error when creating SellDB class {e}")

    def get_schema_version(self):
        try:
            info = self.session.query(InformationSchema).all()
            dt_object = datetime.fromtimestamp(info[0].creation_time)
            version = str(info[0].schema_version) + "-" + str(dt_object)
            return version
        except Exception as e:
            logging.error(f"Could not parse schema version: {e}")
            return "Could parses db schema version"

    def get_nest_record_count(self):
        try:
            count = self.session.query(NestRecord).count()
            return count
        except Exception as e:
            logging.error(f"Could not get records count: {e}")
            return "Could not get records count"

    def insert_nest_record(self, nest_id, weight):
        try:
            record = {
                'nest_id': str(nest_id),
                'weight': str(weight),
                'timestamp': str(datetime.now())}

            dto = map_nestInfo_data_to_dto(record)

            self.session.add(dto)
            self.session.commit()
            pass

        except Exception as e:
            logging.error(f"Could not parse schema version: {e}")

        pass


if __name__ == '__main__':
    CoopMasterDBCreator(host="localhost", port=5432, database="coopmaster", user="coop_admin",
                        password="your_secure_password")