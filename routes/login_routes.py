from flask import Blueprint, request, jsonify
from services.login_service import login

login_routes = Blueprint('login_routes', __name__)

@login_routes.route("/login",methods=['POST'])
def loginUser():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400
    
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    # Harus pastikan login() return dua nilai
    result, code = login(data["email"], data["password"])

    return jsonify(result), code