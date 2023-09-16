from constants import common
from flask import Blueprint, request
from utils.responses import Responses

"""
IMPORT DOMAIN FUNCTIONS :
"""
from api.domain.login_domain import login, otp_verify


LOGIN_BLUEPRINT = Blueprint('login', __name__, url_prefix='/api/v1/')

@LOGIN_BLUEPRINT.route('login', methods=['POST'])
def basic():
    code, message, result = login()

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
    
@LOGIN_BLUEPRINT.route('otp_verify', methods=['POST'])
def otp_verification():
    code, message, result = otp_verify()

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