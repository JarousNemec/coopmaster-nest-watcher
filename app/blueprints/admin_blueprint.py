from flask import Blueprint, make_response

from app.service.nest_watcher_schema.nest_watcher_schema_creator import CoopMasterDBCreator

admin_blueprint = Blueprint('admin_blueprint', __name__)

from app import configuration


@admin_blueprint.route("/api/db/recreate", methods=['GET'])
def recreate_database():
    response = {"state": "recreated"}

    CoopMasterDBCreator(host=configuration.config.DB_HOST,
                        port=configuration.config.DB_PORT,
                        database=configuration.config.POSTGRES_DB,
                        user=configuration.config.POSTGRES_USER,
                        password=configuration.config.POSTGRES_PASSWORD)
    return make_response(response)


@admin_blueprint.route("/api/db/version", methods=['GET'])
def get_schema_version():
    nest_db = configuration.get_nest_db()
    try:
        version = nest_db.get_schema_version()

        response = {"state": version}

        return make_response(response)
    finally:
        nest_db.close()

@admin_blueprint.route("/api/record/count", methods=['GET'])
def get_nest_record_count():
    nest_db = configuration.get_nest_db()
    try:
        count = nest_db.get_nest_record_count()
        response = {"count": count}

        return make_response(response)
    finally:
        nest_db.close()
