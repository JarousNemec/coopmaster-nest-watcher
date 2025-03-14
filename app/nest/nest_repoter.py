import json
import logging
import random

from app import configuration

NESTS_TO_KEEP = configuration.construct_nests_from_env()


def report_nest_data():
    mqtt_client = configuration.get_mqtt_client()
    nest_db = configuration.get_nest_db()
    try:
        if not nest_db.connected:
            raise ConnectionError("Could not connect to nest database")
        mqtt_client.connect()
    except:
        logging.error(
            f"Could not connect to MQTT broker. No data will be published. Check connection to MQTT server. {configuration.config.MQTT_BROKER}:{configuration.config.MQTT_PORT}")
        return

    try:
        ping(mqtt_client, nest_db)
        check_nest_occupacity(mqtt_client, nest_db)
        egg_checker(mqtt_client, nest_db)
    finally:
        nest_db.close()
        mqtt_client.close()


def ping(mqtt_client, nest_db):
    count = nest_db.get_nest_record_count()

    message = {"records_sum": count}
    payload = json.dumps(message)

    result = mqtt_client.publish(configuration.config.MQTT_TOPIC, payload.encode())

    logging.info(f"Going to publish following payload to {configuration.config.MQTT_TOPIC}: {payload.encode()}")
    # Check if the message was successfully published
    status = result[0]
    if status == 0:
        logging.info("Nest status reported successfully")
    else:
        logging.error(f"Nest status reported with error {status}")


def check_nest_occupacity(mqtt_client, nest_db):
    states = ""
    separator = ';'
    for nest in NESTS_TO_KEEP:
        state = "o" if nest_db.get_avarage_weight_for_last_minute(nest["name"]) > configuration.get_chicken_mass() else "f"
        if len(states) > 0:
            states = states + separator
        states = states + str(state)

    result = mqtt_client.publish(configuration.config.MQTT_NEST_STATUS_TOPIC, states.encode())
    status = result[0]
    if status == 0:
        logging.info("Occupancy reported successfully")
    else:
        logging.error(f"Occupancy reported with error {status}")


def egg_checker(mqtt_client, nest_db):
    eggs = ""
    separator = ';'
    for nest in NESTS_TO_KEEP:
        avg_weight = nest_db.get_avarage_weight_for_last_minute(nest["name"])
        count = int(avg_weight/configuration.get_egg_mass()) if avg_weight < configuration.get_chicken_mass() else 0
        if len(eggs) > 0:
            eggs = eggs + separator
        eggs = eggs + str(count)

    result = mqtt_client.publish(configuration.config.MQTT_EGG_COUNT_TOPIC, eggs.encode())
    status = result[0]
    if status == 0:
        logging.info("Eggs reported successfully")
    else:
        logging.error(f"Eggs reported with error {status}")
