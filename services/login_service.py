import jwt
from db import execute_query
import logging
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')

def login(email, password):
    try:
        query = """
        SELECT 
            u.id AS user_id,
            t.id AS teacher_id,
            u.username,
            u.email,
            u.role,
            t.active
        FROM users u
        LEFT JOIN teachers t ON t.user_id = u.id
        WHERE u.email = %s AND u.password = %s;
        """
        values = (email, password)

        result = execute_query(query, values, fetch_one=True)

        if result:
            # Data user
            user_data = {
                'user_id': result['user_id'],
                'teacher_id': result['teacher_id'],
                'username': result['username'],
                'email': result['email'],
                'role': result['role'],
                'active': result['active'],
                'exp': datetime.utcnow() + timedelta(hours=24)  # Expire dalam 24 jam
            }

            # Buat token
            token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')

            logger.info(f"Login berhasil untuk email: {email}")
            return {'message': 'berhasil login','token': token, "valid" : True}, 200
        else:
            logger.warning(f"Login gagal. User tidak ditemukan untuk email: {email}")
            return {'message': 'Invalid email or password', "valid" : False}, 401

    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error', "valid" : False}, 500

def getAdmin(user_id):
    try:
        query = """
        SELECT role
        FROM users
        WHERE id = %s
        """
        
        values = (user_id,)
        
        result = execute_query(query, values, fetch_one=True)
        
        logger.info(f"Check Admin : {result}")
        return {"message": "berhasil cek", "role" : result["role"]},200
    
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500     