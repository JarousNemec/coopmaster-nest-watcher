import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from waitress import serve

from app import configuration
from app.blueprints.admin_blueprint import admin_blueprint
from app.blueprints.weight_blueprint import weight_blueprint
from app.nest.nest_keeper import keep_all_nests
from app.nest.nest_repoter import report_nest_data


def flask_app():
    app = Flask('__main__')

    @app.route("/")
    def hello_world():
        message = "CoopMaster Nest Watcher!"
        logging.info(message)
        return message

    app.register_blueprint(weight_blueprint)
    app.register_blueprint(admin_blueprint)
    return app


def server():
    manager_app = flask_app()

    scheduler = BackgroundScheduler()
    scheduler.add_job(report_nest_data, 'interval', seconds=configuration.config.REPORT_INTERVAL)
    scheduler.add_job(keep_all_nests, 'interval', seconds=configuration.config.REPORT_INTERVAL)
    scheduler.start()

    port = configuration.config.PORT
    host = configuration.config.HOST
    logging.info(f"Serving on http://{host}:{port}")
    logging.info(f"Recreate db on http://{host}:{port}/api/db/recreate")
    serve(manager_app,  port=port)