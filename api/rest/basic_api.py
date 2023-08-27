from constants import common
from flask import Blueprint, request
from utils.responses import Responses

"""
IMPORT DOMAIN FUNCTIONS :
"""
from api.domain.basic_domain import get_basic_data


BASIC_BLUEPRINT = Blueprint('basic', __name__, url_prefix='/api/v1/')

@BASIC_BLUEPRINT.route('basic', methods=['GET'])
def basic():
    code, message, result = get_basic_data()

    if code == 200:
        return Responses.success(
                                code=common['SUCCESS'],
                                alert_msg_description=message,
                                alert_msg_type=common["SUCCESS_ALERT"],
                                result=result
                            )
    else:
        return Responses.failure(
                                code=common['FAILURE'],
                                alert_msg_description=message,
                                alert_msg_type=common["FAILURE_ALERT"],
                                result=result
                            )