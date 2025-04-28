from flask import Blueprint,jsonify
from services.history_service import *
from auth.decorator import token_required


history_routes = Blueprint("history_routes", __name__)


@history_routes.route("/history", methods=['GET'])
@token_required
def historyGetAll(user_id):
    result, code = historyGetAllData()
    return  jsonify(result), code

@history_routes.route("/history/teacher", methods=['GET'])
@token_required
def historyGetAllForOneTeacher(user_id):
    result, code = historyGetAllDataForOneTeacher(user_id)
    return  jsonify(result), code