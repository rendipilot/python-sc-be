from db import execute_query
import logging


logger = logging.getLogger(__name__)

def userUpdateData(data, user_id):
    try:
        query = """
        UPDATE users
        SET email = COALESCE(%s, email)
        WHERE id = %s
        """
        
        values = (data["email"], user_id)
        
        execute_query(query, values)
        
        logger.info("Berhasil mengubah data user")
        return {"message": "berhasil mengubah data user", "valid": True},200
        
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error', "valid": False}, 500

def getPasswordData(user_id):
    try:
        query = """
        SELECT password FROM users
        WHERE id = %s
        """
        
        values = (user_id, )
        
        result = execute_query(query, values, fetch_one=True)
        
        if not result:
            logger.info(f"Password tidak ditemukan {user_id}")
            return {"message": "Password tidak ditemukan"}, 404
        
        logger.info(f"Berhasil mengambil data user {result}")
        return {"message": "berhasil mengambil data user", "oldPassword" : result["password"]},200
        
    except Exception as e:
        logger.error(f"Terjadi error saat proses: {str(e)}")
        return {'message': 'Internal server error'}, 500

def userChangePasswordData(data, user_id):
    try:
        query = """
        UPDATE users
        SET password = %s
        WHERE id = %s
        """
        
        values = (data["newPassword"], user_id)
        
        execute_query(query, values)
        
        logger.info("Berhasil mengubah data user")
        return {"message": "berhasil mengubah data user", "valid": True},200
        
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error', "valid" : False}, 500