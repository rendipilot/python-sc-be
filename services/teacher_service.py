from db import execute_query
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def teacherGetAllData():
    try:
        query = """
        SELECT
        s.id, s.username, s.password, s.email, s.created_at,
        t.active
        FROM teachers t
        LEFT JOIN
        users s ON s.id = t.user_id
        ORDER BY t.active
        """
    
        result = execute_query(query, fetch_all=True)
        
        logger.info("Berhasil dapatkan data guru")
        return {"message": "berhasil dapatkan data guru", "valid": True, "data": result},200
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error',  "valid": False}, 500

def teacherDeleteData(teacher_id):
    try:
        query = """
        UPDATE
        teachers
        SET active = null, deleted_at = %s
        WHERE user_id = %s
        """
        
        values = (datetime.now(),teacher_id,)
    
        execute_query(query, values)
        
        logger.info(f"Berhasil Non-aktifkan guru {teacher_id}")
        return {f"message": "berhasil non aktifkan guru", "valid": True},200
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error', "valid": False}, 500


def teacherActiveData(teacher_id):
    try:
        query = """
        UPDATE
        teachers
        SET active = true
        WHERE user_id = %s
        """
        
        values = (teacher_id,)
    
        execute_query(query, values)
        
        logger.info("Berhasil aktifkan guru")
        return {"message": "berhasil aktifkan guru", "valid": True},200
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error', "valid": False}, 500


def teacherAddData(data):
    try:
        query = """
        WITH new_user AS (
            INSERT INTO users (username, email, password, role, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        )
        INSERT INTO teachers (user_id, active, created_at, updated_at)
        SELECT id, true, %s, %s FROM new_user;
        """
        
        values = (data["username"], data["email"], data["password"], "teacher", datetime.now(), datetime.now(),datetime.now(),datetime.now())
        
        execute_query(query, values)
        
        logger.info("Berhasil menambahkan data guru")
        return {"message": "berhasil menambahkan data guru", "valid": True},200
    
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error', "valid": False}, 500
  

def teacherUpdateData(data):
    try:
        query = """
         UPDATE users 
         SET 
         username = COALESCE(%s, username), email = COALESCE(%s, email), password=COALESCE(%s, password), updated_at =%s  
         WHERE id = %s      
        """
        
        values = (data["username"], data["email"], data["password"], datetime.now(), data["teacher_id"])
        
        execute_query(query, values)
        
        logger.info("Berhasil mengubah data guru")
        return {"message": "berhasil mengubah data guru", "valid": True},200
    
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error', "valid": False}, 500