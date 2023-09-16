import random
from flask_sqlalchemy_session import current_session as session
from flask import g, request
from constants import common
from api.db.login_db import Otp, Users
import uuid
def login():
    try:
        data = request.json
        email = data.get('email', None)
        password = data.get('password', None)
        phone_number = data.get('phone_number', None)

        if phone_number:
            otp =  random.randint(1000, 9999)
            user_id = uuid.uuid4()
            print(user_id)
            user_db = Users(
                user_id=user_id,
                phone_number=phone_number
            )
            user_db.save()
            
            otp_db = Otp(
                user_id=user_id,
                otp=otp
            )
            otp_db.save()
            response = {}
            response["phone_number"] = phone_number
            response["OTP"] = otp
            return 200, common["SUCCESS"], response

        return 200, "SUCESS", {
            "email": email,
            "password": password
        }
    except Exception as e:
        return 400, "BAD_REQUEST", str(e)

def otp_verify():
    data = request.json
    otp= data.get("otp", None)

    otp_db = session.query(otp).filter(Otp.user_id=="test").first()
    if otp_db:
        if otp_db.otp == otp:
            return 200, common["SUCCESS"], {"otp": otp}
        else:
            return 400, "BAD_REQUEST", {}
    
    