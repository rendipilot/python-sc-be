from db import execute_query
import logging

logger = logging.getLogger(__name__)

def teacherGetAllData():
    try:
        query = """
        SELECT
        s.username, s.email, s.created_at,
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