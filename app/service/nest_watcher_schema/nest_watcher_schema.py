import logging
import time

import sqlalchemy
from sqlalchemy import text


from app.service.common_schema.database import FajneBase
from app.service.nest_watcher_schema.information_schema import InformationSchema
from app.service.nest_watcher_schema.nest_record import NestRecord
from app.service.nest_watcher_schema.sell import Sell


def create_information_schema_table(engine, db_session):
    exist = sqlalchemy.inspect(db_session.bind).has_table("information_schema")
    if not exist:
        InformationSchema.__table__.create(engine)
    else:
        # assert False
        pass


def create_sell_table(engine, db_session):
    exist = sqlalchemy.inspect(db_session.bind).has_table("sell")
    if not exist:
        Sell.__table__.create(engine)
    else:
        # assert False
        pass

def create_nest_record_table(engine, db_session):
    exist = sqlalchemy.inspect(db_session.bind).has_table("nest_record")
    if not exist:
        NestRecord.__table__.create(engine)
    else:
        # assert False
        pass


def create_nest_watcher_db_schema(engine, db_session):
    with db_session as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()

    FajneBase.metadata.create_all(db_session.bind)

    create_information_schema_table(engine, db_session)
    create_sell_table(engine, db_session)
    create_nest_record_table(engine, db_session)

    query = ["CREATE ROLE rds WITH LOGIN;",
             "CREATE ROLE tesco_admin WITH LOGIN;",

             "ALTER DATABASE fajne OWNER TO fajne_admin;",
             "ALTER DATABASE fajne OWNER TO rds;",

             "GRANT ALL ON SCHEMA public TO fajne_admin",
             "GRANT ALL ON SCHEMA public TO fajne_admin",

             "GRANT SELECT ON ALL TABLES IN SCHEMA public TO fajne_admin;",
             "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO fajne_admin;",

             "GRANT SELECT ON ALL TABLES IN SCHEMA public TO rds;",
             "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO rds;",
             "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO rds;",
             ]

    for q in query:
        run_sql_query(db_session, q)
    db_session.commit()


def run_sql_query(db_session, query):
    try:
        with db_session as conn:
            conn.execute(text(query))
            conn.commit()
    except Exception as e:
        logging.error(e)


def insert_schema_version(db_session):
    schema = InformationSchema(schema_version=1, creation_time=time.time())
    db_session.add(schema)
    db_session.commit()
