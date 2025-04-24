from functools import wraps
import os
from flask import request, jsonify
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Missing Authorization Header"}), 401

        try:
            token = auth_header.split(" ")[1]  # "Bearer <token>"
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Simpan decoded token ke kwargs supaya bisa diakses di route
            kwargs['user_id'] = decoded.get("user_id")
            # kwargs['user'] = decoded  # Kalau mau simpan semua info user
        except ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": "Token error", "message": str(e)}), 401

        return f(*args, **kwargs)
    return decorated
