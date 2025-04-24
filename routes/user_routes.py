from flask import Blueprint, request, jsonify
from auth.decorator import token_required
from services.user_service import *

user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/user/update", methods=["PUT"])
@token_required
def userUpdate(user_id):
    data = request.get_json()
    result,code = userUpdateData(data)
    return jsonify(result), code


@user_routes.route("/user/change-password", methods=["PUT"])
@token_required
def userChangePassword(user_id):
    data = request.get_json()
    result, code = getPasswordData(data)
    
    if data["oldPassword"] == data["newPassword"]:
        return jsonify({"message" : "password baru dan lama tidak boleh sama"}), 200
    
    if code == 404:
        return jsonify(result), 200
    
    if code == 500:
        return jsonify(result), code
    
    result, code = userChangePasswordData(data)
    return jsonify(result), code