from flask import Blueprint, request, jsonify
from auth.decorator import token_required
from services.teacher_service import *
from services.login_service import getAdmin


teacher_routes = Blueprint('teacher_routes', __name__)

@teacher_routes.route("/teacher", methods=['GET'])
@token_required
def teacherGetAll(user_id):
    isAdmin, code = getAdmin(user_id)
    
    if code != 200:
        return jsonify({"message" : "kesalahan auth"}), code
    
    if isAdmin["role"] != "admin":
         return jsonify({"message" : "tidak di izinkan"}), 301
    result, code = teacherGetAllData()
    
    return jsonify(result),code

@teacher_routes.route("/teacher/delete", methods=["PUT"])
@token_required
def teacherDeleted(user_id):
    isAdmin, code = getAdmin(user_id)
    
    if code != 200:
        return jsonify({"message" : "kesalahan auth"}), code
    
    if isAdmin["role"] != "admin":
         return jsonify({"message" : "tidak di izinkan"}), 301
    
    data = request.get_json()
    result, code = teacherDeleteData(data.get('teacher_id'))
    
    return jsonify(result), code


@teacher_routes.route("/teacher/aktif", methods=["PUT"])
@token_required
def teacherActivated(user_id):
    isAdmin, code = getAdmin(user_id)
    
    if code != 200:
        return jsonify({"message" : "kesalahan auth"}), code
    
    if isAdmin["role"] != "admin":
         return jsonify({"message" : "tidak di izinkan"}), 301
    
    data = request.get_json()
    result, code = teacherActiveData(data.get('teacher_id'))
    
    return jsonify(result), code

@teacher_routes.route("/teacher/add", methods=['POST'])
@token_required
def teacherAdded(user_id):
    isAdmin, code = getAdmin(user_id)
    
    if code != 200:
        return jsonify({"message" : "kesalahan auth"}), code
    
    if isAdmin["role"] != "admin":
         return jsonify({"message" : "tidak di izinkan"}), 301
    
    data = request.get_json()
    result, code = teacherAddData(data)
    
    return jsonify(result), code

@teacher_routes.route("/teacher/update", methods=['PUT'])
@token_required
def teacherUpdated(user_id):
    isAdmin, code = getAdmin(user_id)
    
    if code != 200:
        return jsonify({"message" : "kesalahan auth"}), code
    
    if isAdmin["role"] != "admin":
         return jsonify({"message" : "tidak di izinkan"}), 301
    
    data = request.get_json()
    result, code = teacherUpdateData(data)
    
    return jsonify(result), code