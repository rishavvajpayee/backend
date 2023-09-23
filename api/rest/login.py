from constants import common
from flask import Blueprint, request
from utils.responses import Responses, response_success, response_failure

"""
IMPORT DOMAIN FUNCTIONS :
"""
from api.domain.onboarding_domain import login, otp_verify, signup


LOGIN_BLUEPRINT = Blueprint("login", __name__, url_prefix="/api/v1/")


@LOGIN_BLUEPRINT.route("signup", methods=["POST"])
def post_signup():
    code, message, result = signup()

    if code == 200:
        return response_success(message, result)

    else:
        return response_failure(message, result)


@LOGIN_BLUEPRINT.route("login", methods=["POST"])
def post_login():
    code, message, result = login()

    if code == 200:
        return response_success(message, result)

    else:
        return response_failure(message, result)


@LOGIN_BLUEPRINT.route("otp_verify", methods=["POST"])
def otp_verification():
    code, message, result = otp_verify()

    if code == 200:
        return response_success(message, result)

    else:
        return response_failure(message, result)
