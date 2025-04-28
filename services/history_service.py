from db import execute_query
import logging

logger = logging.getLogger(__name__)

def historyGetAllDataForOneTeacher(user_id):
    try:
        query = """
        SELECT 
        h.id, h.name, h.user_id, s.username, h.creativity_score, h.logical_score, h.complexity_score,
        h.level_score, h.created_at
        FROM 
        histories h LEFT JOIN users s ON h.user_id = s.id 
        WHERE h.user_id = %s
        ORDER BY 
        h.created_at DESC;
        """
        
        values = (user_id,)
        
        result = execute_query(query, values, fetch_all=True)
        logger.info("berhasil mendapatkan data history")
        return {'message' : 'berhasil mendapatkan data history', 'data' : result}, 200
    
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500

def historyGetAllData():
    try:
        query = """
        SELECT 
        h.id, h.name, h.user_id, s.username, h.creativity_score, h.logical_score, h.complexity_score,
        h.level_score, h.created_at
        FROM 
        histories h LEFT JOIN users s
        ON h.user_id = s.id
        """
        
        result = execute_query(query, fetch_all=True)
        logger.info("berhasil mendapatkan data history")
        return {'message' : 'berhasil mendapatkan data history', 'data' : result}, 200
    
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500