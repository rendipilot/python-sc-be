from flask import Blueprint, request, jsonify, make_response
import jwt, os
from services.login_service import login, isActive
import logging

login_routes = Blueprint('login_routes', __name__)

SECRET_KEY = os.getenv('SECRET_KEY')
logger = logging.getLogger(__name__)

@login_routes.route("/me",methods=["GET"])
def hello():
    token = request.cookies.get('mkm-token')
    if not token:
        logger.info(f"token  tidak ditemukan = {token}")
        response = make_response(jsonify({"error": "Token not found"}), 401)
        response.set_cookie('token', '', expires=0)
        return response

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        active = isActive(payload.get("user_id"))
        
        
        if(active == 401):
            response = make_response(jsonify({"error": "Akun sudah dibanned"}), 401)
            response.set_cookie('mkm-token', '', expires=0)
            logger.info("akun sudah dibanned")
            return response
        
        logger.info("jwt dikirimkan")
        return jsonify({
            "user_id": payload.get("user_id"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "role": payload.get("role"),
            "active": payload.get("active"),
        })
        
    except jwt.ExpiredSignatureError:
        # Token sudah expired, hapus cookie dan beri error
        response = make_response(jsonify({"error": "Token expired"}), 401)
        response.set_cookie('mkm-token', '', expires=0)
        logger.info("token sudah expired")
        return response
    except jwt.InvalidTokenError:
        # Token tidak valid, hapus cookie dan beri error
        response = make_response(jsonify({"error": "Invalid token"}), 401)
        response.set_cookie('mkm-token', '', expires=0)
        logger.info("token tidak valid")
        return response

@login_routes.route("/login",methods=['POST'])
def loginUser():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Request body must be JSON", "valid": False}), 400
    
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required", "valid": False}), 400
    
    # Harus pastikan login() return dua nilai
    result, code = login(data["email"], data["password"])

    if code == 200:
        token = result.get("token")
        response = make_response(jsonify({"message": "berhasil login", "valid": True}), 200)

        # Set cookie: nama = token, aman dan HttpOnly
        response.set_cookie(
            "mkm-token", 
            token,
            httponly=True,
            max_age=60 * 60 * 24 , # 1 hari
            samesite='Lax',
            path='/',
        )
        return response

    return jsonify(result), code


@login_routes.route("/logout", methods=['POST'])
def logoutUser():
    response = make_response(jsonify({"message": "Logged out successfully", "valid": True}), 200)
    # Menghapus cookie token
    response.set_cookie("mkm-token", "", expires=0, path='/')  # Menghapus cookie dengan cara ini
    return response