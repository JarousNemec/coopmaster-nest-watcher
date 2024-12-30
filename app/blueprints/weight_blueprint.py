import json
import logging
from datetime import datetime

from flask import Blueprint, request, jsonify, make_response

weight_blueprint = Blueprint('weight_blueprint', __name__)



@weight_blueprint.route("/api/weight", methods=['GET'])
def get_weight_endpoint():
    response = {"weight_1": 0.1245}
    return make_response(response)



