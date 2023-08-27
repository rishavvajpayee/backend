"""

from flask import request
from utils.responses import Response
from conf.database import Config

def validate_token(user_token, endpoint):
    from .redis_connection import redis_client
    import json
    app_token = redis_client.get(Config.APPLICATION_ID)
    if not app_token:
        authenticate_url = Config.AUTHENTICATION_BASE_URL + '/api/v1/authenticate/micro_service'
        auth_payload = {"application_id": str(Config.APPLICATION_ID)}
        auth_code, auth_resp = make_api_call(method_type='POST', url=authenticate_url, json=auth_payload,
                                             no_header=True,
                                             internal=True)
        if auth_code != 200:
            return False

        if auth_code == 200:
            json_resp = auth_resp.json()
            app_token = json_resp["data"]["access_token"]
            cache_access_token(Config.APPLICATION_ID, app_token)
            # header = {"accesstoken": data["access_token"]}

    user_access_token = redis_client.keys('*' + user_token)
    if user_access_token:
        user_access_token = redis_client.get(user_access_token[0])
        user_access_token = json.loads(user_access_token)
        g.user_id = user_access_token["user_id"]
        g.device_id = user_access_token["device_id"]
        g.application_id = user_access_token['application_id']
        g.application_name = user_access_token["application_name"]
        g.cms_user_name = user_access_token["cms_user_name"]
        g.cms_user_email = user_access_token["cms_user_email"]
        g.cms_user_mobile = user_access_token["cms_user_mobile"]
        g.accesstoken = user_token
        g.app_access_token = app_token
        return True
    else:
        header = {"accesstoken": app_token}
        payload = {'token': user_token, 'endpoint': endpoint}
        validate_url = Config.AUTHENTICATION_BASE_URL + '/api/v1/validate/token'
        code, response = make_api_call(method_type='POST', url=validate_url, json=payload, internal=True, header=header)
        if code == 200:
            json_resp = response.json()
            if not "data" in json_resp:
                return True
            data = json_resp["data"]
            g.user_id = data["user_id"]
            g.device_id = data["device_id"]
            g.application_id = data['application_id']
            g.application_name = data["application_name"]
            g.cms_user_name = data["cms_user_name"]
            g.cms_user_email = data["cms_user_email"]
            g.cms_user_mobile = data["cms_user_mobile"]
            g.accesstoken = user_token
            g.app_access_token = app_token
            key = g.user_id + str(g.device_id) + user_token
            cache_access_token(key, data, True)
            return True
        else:
            return False

def before_check():
    if 'X-Forwarded-Proto' in request.headers and request.headers['X-Forwarded-Proto'] == 'http':
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
    g.request_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    url = request.path
    whitelistApi = Config.WHITELIST_API.split(",") if Config.WHITELIST_API else []
    if request.method == "OPTIONS" or url in whitelistApi:
        return
    if 'Accesstoken' in request.headers:
        token = request.headers['Accesstoken']
        if 'internal_api' in request.headers and request.headers['internal_api'] == '1':
            internal_call = validate_internal_api(token)
        else:
            validated_token = validate_token(token, request.path)
            if not validated_token:
                return responses.failure(code=401,
                                         alert_msg_description="Token validation failed",
                                         alert_msg_type=common["FAILURE_ALERT"],
                                         result={})
    else:
        return responses.failure(code=401,
                                 alert_msg_description="Token is missing",
                                 alert_msg_type=common["FAILURE_ALERT"],
                                 result={})

def after_check(response):
    if request.method == "OPTIONS":
        return Response()
    response_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    logging_enable = int(Config.LOG_ENABLE) if Config.LOG_ENABLE else 0
    if logging_enable and not request.path == '/api/is_alive':
        log_data(request, response, g.request_time, response_time)
    response.headers['Server'] = 'Application Server'
    response.headers['Strict-Transport-Security'] = 'max-age=16070400 ; includeSubDomains'
    response.headers['X-Frame-Options'] = 'deny'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = 'script-src "self"'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers[
        'Feature-Policy'] = "vibrate 'none'; geolocation 'none'; midi 'none'; notifications 'none'; push 'none'; sync-xhr 'none'; camera 'none'; microphone 'none'; speaker 'none'; magnetometer 'none'; gyroscope 'none'; fullscreen 'none'; payment 'none'"
    response.headers['Cache-Control'] = 'private, no-cache, no-store, max-age=0, no-transform'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0
    return response


def validate_internal_api(token):
    from .redis_connection import redis_client
    import json
    app_token = redis_client.get(Config.APPLICATION_ID)
    if app_token:
        return True
    else:
        authenticate_url = Config.AUTHENTICATION_BASE_URL + '/api/v1/authenticate/micro_service'
        auth_payload = {"application_id": str(Config.APPLICATION_ID)}
        auth_code, auth_resp = make_api_call(method_type='POST', url=authenticate_url, json=auth_payload,
                                             no_header=True,
                                             internal=True)
        if auth_code != 200:
            return False

        if auth_code == 200:
            json_resp = auth_resp.json()
            app_token = json_resp["data"]["access_token"]
            cache_access_token(Config.APPLICATION_ID, app_token)
            return True

"""