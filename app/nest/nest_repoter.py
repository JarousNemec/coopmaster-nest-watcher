import json
import logging

from app import configuration

def report_nest_data():
    count = configuration.get_nest_db().get_nest_record_count()

    message = {"count": count}
    payload = json.dumps(message)

    mqtt_client = configuration.get_mqtt_client()
    try:
        mqtt_client.connect()
    except:
        logging.error(f"Could not connect to MQTT broker. No data will be published. Check connection to MQTT server. {configuration.config.MQTT_BROKER}:{configuration.config.MQTT_PORT} {configuration.config.MQTT_TOPIC} ")
        return

    result = mqtt_client.publish(configuration.config.MQTT_TOPIC, payload.encode())
    logging.info(f"Going to publih following payload to {configuration.config.MQTT_TOPIC}: {payload.encode()}")

    # Check if the message was successfully published
    status = result[0]
    if status == 0:
        print("ok")
    else:
        print("failed")
