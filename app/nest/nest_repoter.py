import json
import logging
import random

from app import configuration


def report_nest_data():
    mqtt_client = configuration.get_mqtt_client()
    nest_db = configuration.get_nest_db()
    try:
        mqtt_client.connect()
    except:
        logging.error(
            f"Could not connect to MQTT broker. No data will be published. Check connection to MQTT server. {configuration.config.MQTT_BROKER}:{configuration.config.MQTT_PORT} {configuration.config.MQTT_TOPIC} ")
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

    message = {"count": count}
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
    topic = f"nests/status"
    states = ""
    separator = ';'
    for i in range(0, 6):
        state = "o" if random.randint(1, 100) < 50 else "f"
        if len(states) > 0:
            states = states + separator
        states = states + str(state)

    result = mqtt_client.publish(topic, states.encode())
    status = result[0]
    if status == 0:
        logging.info("Occupancy reported successfully")
    else:
        logging.error(f"Occupancy reported with error {status}")


def egg_checker(mqtt_client, nest_db):
    for i in range(1, 7):
        broker = f"nests/{i}/egg"
        state = {
            "state": "on",
            "attributes": {
                "device_class": "occupancy"
            }
        }
        payload = json.dumps(state)
        result = mqtt_client.publish(broker, payload.encode())
        status = result[0]
        if status == 0:
            logging.info("Eggs reported successfully")
        else:
            logging.error(f"Eggs reported with error {status}")
