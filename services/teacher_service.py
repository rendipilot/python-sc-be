from db import execute_query
import logging

logger = logging.getLogger(__name__)

def teacherGetAllData():
    try:
        query = """
        SELECT
        t.id, s.username, s.email, s.created_at,
        t.active
        FROM teachers t
        LEFT JOIN
        users s ON s.id = t.user_id
        """
    
        result = execute_query(query, fetch_all=True)
        
        logger.info("Berhasil dapatkan data guru")
        return {"message": "berhasil dapatkan data guru", "data": result},200
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500

def teacherDeleteData(teacher_id):
    try:
        query = """
        UPDATE
        teachers
        SET active = false
        WHERE id = %s
        """
        
        values = (teacher_id,)
    
        execute_query(query, values)
        
        logger.info("Berhasil Non-aktifkan guru")
        return {"message": "berhasil non aktifkan guru"},200
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500


def teacherActiveData(teacher_id):
    try:
        query = """
        UPDATE
        teachers
        SET active = true
        WHERE id = %s
        """
        
        values = (teacher_id,)
    
        execute_query(query, values)
        
        logger.info("Berhasil aktifkan guru")
        return {"message": "berhasil aktifkan guru"},200
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500
