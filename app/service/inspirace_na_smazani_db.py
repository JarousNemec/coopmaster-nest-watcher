import logging
import random
import time
from datetime import datetime, timedelta

from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.orm import sessionmaker


from app.service.nest_watcher_schema.information_schema import InformationSchema
from app.service.nest_watcher_schema.nest_watcher_schema_creator import CoopMasterDBCreator
from app.service.nest_watcher_schema.sell import Sell


class FajneSellDB:

    def __init__(self, host, port, database, user, password):
        try:
            conn_string = f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}'
            engine = create_engine(conn_string)
            self.engine = engine
            session = sessionmaker(bind=engine)
            self.session = session()
        except Exception as e:
            logging.error(f"Error when creating SellDB class {e}")

    def insert_sell(self, new_sell):
        try:
            self.session.add(new_sell)
            self.session.commit()
        except Exception as e:
            logging.error(f"Error when adding new device: {e}")

    def list_sells(self):
        try:
            new_sells = self.session.query(Sell).all()
            return new_sells
        except Exception as e:
            logging.error(f"Error when listing archive files {e}")

    def get_schema_version(self):
        try:
            info = self.session.query(InformationSchema).all()
            dt_object = datetime.fromtimestamp(info[0].creation_time)
            version = str(info[0].schema_version) + "-" + str(dt_object)
            return version
        except Exception as e:
            logging.error(f"Could not parse schema version: {e}")
            return "Could parses db schema version"

    def get_tables_count(self):
        logging.info("Method get_tables_count() invoked.")
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        table_names = metadata.tables.keys()

        # Count the number of tables
        table_count = len(table_names)

        logging.info("get_tables_count() done.")

        return str(table_count) + f" - {table_names}"

    def get_sell_count(self):
        rows = self.session.query(Sell).count()
        return rows

    def delete_all_sell(self):
        try:
            self.session.query(Sell).delete()
            self.session.commit()
        except Exception as e:
            logging.error(f"Error when deleting all Sells: {e}")

    def get_sell_per_device_and_day(self):

        try:
            start = datetime.now()
            # TODO select this year
            result = (
                self.session.query(func.extract('doy', Sell.transaction_timestamp).label('day_of_year'), Sell.device_id,
                                   func.count(Sell.suggestion_id)).group_by('day_of_year', Sell.device_id).all())

            # TODO alias performance
            # solve issue with actual year
            actual_year = 2024

            device_stats = {}
            for row in result:
                to_date = self.convert_date_of_the_year(int(row[0]), actual_year)
                alias = row[1]
                count = row[2]

                if alias in device_stats:
                    day_stat = [to_date, count]
                    device_stats[alias].append(day_stat)
                else:
                    day_stat = [[to_date, count]]
                    device_stats[alias] = day_stat

            end = datetime.now()
            logging.info(f"SQLQuery -  get_scale_with_no_sell - time elapsed: {end - start}")
            return device_stats
        except Exception as e:
            logging.error(f"Could not retrieve data for get_sell_per_scale_and_day(): {e}")

        return {}

    def convert_date_of_the_year(self, day_of_year, year):
        from datetime import datetime
        date_object = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
        date_string = date_object.strftime("%Y-%m-%d")

        return date_string

    def get_daily_sell_per_PLU(self):
        data = []
        try:
            result = (
                self.session.query(
                    func.extract('week', Sell.transaction_timestamp).label('day_of_year'),
                    func.count(Sell.suggestion_id),
                    Sell.sold_assorment
                ).group_by('day_of_year', Sell.sold_assorment)
                .order_by("day_of_year")
                .all()
            )

            for row in result:
                data.append({
                    "week": row[0],
                    "date": "--",
                    "item_id": row[2],
                    "description": "--",
                    "count": row[1],
                    "match": "--",
                })

        except Exception as e:
            logging.error(f"Could not retrieve daily sell_per_PLU(): {e}.")

        total = self.get_sell_count()
        return data, total

    def get_match_rate(self):

        days = 30

        try:

            current_time = datetime.now()
            days_ms = current_time - timedelta(days=days)
            condition = (Sell.transaction_timestamp >= days_ms)

            matching_count = self.session.query(Sell.sold_assorment, func.count()).filter(condition).filter(
                (Sell.pos1 == Sell.sold_assorment) |
                (Sell.pos2 == Sell.sold_assorment) |
                (Sell.pos3 == Sell.sold_assorment) |
                (Sell.pos4 == Sell.sold_assorment) |
                (Sell.pos5 == Sell.sold_assorment)
            ).group_by(Sell.sold_assorment).all()

            found = {}

            for row in matching_count:
                found[row[0]] = row[1]

            all_count = (self.session.query(Sell.sold_assorment, func.count())
                              .filter(condition).
                              group_by(Sell.sold_assorment).all())

            total = {}

            for row in all_count:
                total[row[0]] = row[1]

            data = []
            for key in total.keys():

                success = 0
                if key in found:
                    success = found[key]

                item = {
                    "plu": key,
                    "sold": total[key],
                    "success": success,
                    "match": (float(success) / float(total[key])) * 100,
                }
                data.append(item)

            return data
        except Exception as e:
            logging.error(f"Could not retrieve daily sell_per_PLU(): {e}.")


def add_data(get_fajne_sell_db):
    try:
        sug_id = 1000
        for device in range(1, 10):
            for i in range(1, 10):
                ra = random.randint(1, 100)
                for per_day in range(1, ra):
                    sell = Sell(
                        suggestion_id="sug_" + str(sug_id),
                        sell_id='sell_id',
                        device_id=f'dev-{device}',
                        sold_assorment=f'pos{device}',
                        neural_duration=100,
                        transaction_duration=100,
                        transaction_timestamp=datetime.now().date() - timedelta(days=i),
                        pos1='pos1',
                        sug1=50,
                        pos2='pos2',
                        sug2=10,
                        pos3='pos3',
                        sug3=9,
                        pos4='pos4',
                        sug4=8,
                        pos5='pos5',
                        sug5=1
                    )
                    get_fajne_sell_db.insert_sell(sell)
                    sug_id += 1
    except Exception as e:
        print(e)


if __name__ == '__main__':
    CoopMasterDBCreator(host="localhost", port=5432, database="coopmaster", user="rds",
                        password="aviate_puzzle_alms_chick")

    # fajne_sell_db = FajneSellDB(host="localhost", port=5432, database="coop", user="coop_admin",
    #                             password="aviate_puzzle_alms_chick")
    #
    # print( "Schema version: " +  fajne_sell_db.get_schema_version())
