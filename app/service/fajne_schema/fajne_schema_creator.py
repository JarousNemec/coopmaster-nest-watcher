import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.service.fajne_schema.fajne_schema import create_fajne_db_schema, insert_schema_version


class CoopMasterDBCreator:
    def __init__(self, host, port, database, user, password):
        logging.info(f"Connecting to {host}:{port}")
        logging.info("Going to create db schema - CoopMasterDBCreator")
        try:
            engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}')
            session = sessionmaker(bind=engine)
            create_fajne_db_schema(engine, session())
            insert_schema_version(session())
            logging.info("Schema CoopMasterDBCreator created  ")
        except Exception as e:
            logging.error(f"Error creating db schema CoopMasterDBCreator: {e}")
