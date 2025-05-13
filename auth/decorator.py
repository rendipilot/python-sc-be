from functools import wraps
import os
from flask import request, jsonify, make_response
from services.login_service import isActive
import jwt
import logging
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = os.getenv('SECRET_KEY')
logger = logging.getLogger(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('mkm-token')
        if not token:
            logger.info(f"token  tidak ditemukan = {token}")
            response = make_response(jsonify({"error": "Token not found"}), 401)
            response.set_cookie('token', '', expires=0)
            return response
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        active = isActive(payload.get("user_id"))
        
        if(active == 401):
            response = make_response(jsonify({"error": "Akun sudah dibanned"}), 401)
            response.set_cookie('mkm-token', '', expires=0)
            logger.info("akun sudah dibanned")
            return response

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Simpan decoded token ke kwargs supaya bisa diakses di route
            kwargs['user_id'] = decoded.get("user_id")
            # kwargs['user'] = decoded  # Kalau mau simpan semua info user
        except jwt.ExpiredSignatureError:
            response = make_response(jsonify({"error": "Token expired"}), 401)
            response.set_cookie('mkm-token', '', expires=0)
            logger.info("token sudah expired")
            return response
        except jwt.InvalidTokenError:
            response = make_response(jsonify({"error": "Invalid token"}), 401)
            response.set_cookie('mkm-token', '', expires=0)
            logger.info("token tidak valid")
            return response

        return f(*args, **kwargs)
    return decorated
