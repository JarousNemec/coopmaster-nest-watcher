from random import randrange

import requests
import logging

from app import configuration

NESTS_TO_KEEP = configuration.construct_nests_from_env()


def parse_values(input_str):
    # Split the string by ';' and get the first part
    parts = input_str.split(';')
    time_part = parts[0]

    # weight comes in grams
    weight_part = parts[1]

    weight = abs(int(float(weight_part)))
    return time_part, weight


def keep_all_nests():
    nest_db = configuration.get_nest_db()
    if not nest_db.connected:
        logging.error('Could not connect to Nest database.')
        return
    try:
        for nest in NESTS_TO_KEEP:
            name = nest["name"]
            ip = nest["ip"]
            port = nest["port"]
            enabled = nest["enabled"]
            logging.info(f"NestKeeper is keeping {name}")

            if not enabled:
                nest_db.insert_nest_record(nest_id=name, weight=-1)
                continue

            # each scale endpoint is identified by port of the endpoint
            url = f'http://{ip}:{port}/api/weight'
            try:
                response = requests.get(url, timeout=0.5)

                # Check if the request was successful
                if response.status_code == 200:
                    # Print the content of the response
                    data = response.text
                    date, weight = parse_values(data)

                    logging.info(f"Nest: {name} - time: {date} - weight: {weight} g.")
                    nest_db.insert_nest_record(nest_id=name, weight=weight)
                else:
                    logging.error(f'Failed to retrieve data: {response.status_code}')

            except requests.exceptions.RequestException as e:
                logging.error(f'Can not connect to nest driver application {url}')

        logging.info("All nests checked.")
    finally:
        nest_db.close()
