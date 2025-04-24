from flask import Blueprint, request, jsonify
from auth.decorator import token_required
from services.teacher_service import teacherGetAllData


teacher_routes = Blueprint('teacher_routes', __name__)

@teacher_routes.route("/teacher", methods=['GET'])
@token_required
def teacherGetAll(user_id):
    result, code = teacherGetAllData()
    
    return jsonify(result),code