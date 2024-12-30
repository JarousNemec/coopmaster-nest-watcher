from app import configuration

from app.logging.hen_logger import init_logger
from app.server import server
from app.service.fajne_schema.fajne_schema_creator import CoopMasterDBCreator

init_logger()

def start_server():
    server()


if __name__ == '__main__':
    print("Starting nest Watcher ")
    start_server()
