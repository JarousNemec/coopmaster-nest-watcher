import os
from typing import Union, get_type_hints

from flask.cli import load_dotenv
from app.mqqt_client import NestMQTTClient
from app.service.nest_db import NestSellDB

log_file_name = "nest_watcher.log"

load_dotenv()

def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']


class AppConfigError(Exception):
    pass


class AppConfig:
    PORT: int = 10000
    HOST: str = "127.0.0.1"
    INSTALLATION_DIRECTORY: str = "/bizstorecard"

    DB_HOST: str = "coop-solution-db"
    DB_PORT: int = 5432

    POSTGRES_USER: str = "coop_admin"
    POSTGRES_PASSWORD: str = "your_secure_password1"
    POSTGRES_DB: str = "coopmaster"

    MQTT_BROKER: str = "192.168.1.177"
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "/nest_watcher/count"
    MQTT_NEST_STATUS_TOPIC: str = "coopmaster/nests/status"
    MQTT_EGG_COUNT_TOPIC: str = "coopmaster/eggs/count"
    REPORT_INTERVAL: int = 5

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """

    def __init__(self, env):

        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError('Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                )
                )

    def __repr__(self):
        return str(self.__dict__)


config = AppConfig(os.environ)


def construct_nests_from_env():
    nests = []
    # Iterate through environment variables to collect nest data
    for i in range(1, 7):  # Assuming you have six nests
        name = f"NEST_{i}"
        ip = os.getenv(f"{name}_IP")
        port = os.getenv(f"{name}_PORT")
        enabled = os.getenv(f"{name}_ENABLED")

        # Construct each nest's dictionary
        if ip and port and enabled is not None:
            nests.append({
                "name": f"nest_{i}",
                "ip": ip,
                "port": int(port),
                "enabled": enabled.upper() == 'TRUE'
            })

    return nests

# Use the function
nests = construct_nests_from_env()

# Print out the nests to verify
print(nests)


def get_mqtt_client():
    return NestMQTTClient(
        config.MQTT_BROKER,
        config.MQTT_PORT,
        config.MQTT_TOPIC
    )


def get_nest_db():
    return NestSellDB(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )


def get_log_directory():
    return "./logs/"


def get_log_filename():
    return log_file_name
