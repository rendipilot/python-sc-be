from flask import Blueprint, request, jsonify
from auth.decorator import token_required
from services.user_service import *
import re

user_routes = Blueprint('user_routes', __name__)

password_regex = r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$"
email_regex = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"

@user_routes.route("/user/update", methods=["PUT"])
@token_required
def userUpdate(user_id):
    data = request.get_json()
    
    if not re.match(email_regex, data["email"]):
        return jsonify({"message": "Email harus menggunakan domain @gmail.com", "valid": False}), 200
    
    result,code = userUpdateData(data, user_id)
    return jsonify(result), code


@user_routes.route("/user/change-password", methods=["PUT"])
@token_required
def userChangePassword(user_id):
    data = request.get_json()
    result, code = getPasswordData(user_id)
    
    if data["oldPassword"] != result["oldPassword"]:
        return jsonify({"message" : "password lama anda tidak valid", "valid": False}), 200
    
    if data["oldPassword"] == data["newPassword"]:
        return jsonify({"message" : "password baru dan lama tidak boleh sama", "valid": False}), 200
    
    if not re.match(password_regex, data["newPassword"]):
        return jsonify({"message": "Password baru harus memiliki minimal 8 karakter, satu huruf besar, satu angka, dan satu karakter unik.", "valid": False}), 200
    
    if code == 404:
        return jsonify(result), 200
    
    if code == 500:
        return jsonify(result), code
    
    result, code = userChangePasswordData(data, user_id)
    return jsonify(result), code