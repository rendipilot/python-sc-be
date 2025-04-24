from db import execute_query
import logging


logger = logging.getLogger(__name__)

def userUpdateData(data):
    try:
        query = """
        UPDATE users
        SET username = COALESCE(%s, username), email = COALESCE(%s, email)
        WHERE id = %s
        """
        
        values = (data["username"], data["email"], data["user_id"])
        
        execute_query(query, values)
        
        logger.info("Berhasil mengubah data user")
        return {"message": "berhasil mengubah data user"},200
        
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500

def getPasswordData(data):
    try:
        query = """
        SELECT password FROM users
        WHERE id = %s
        """
        
        values = (data["user_id"], )
        
        result = execute_query(query, values, fetch_one=True)
        
        if not result:
            logger.info(f"Password tidak ditemukan {data["user_id"]}")
            return {"message": "Password tidak ditemukan"}, 404
        
        logger.info("Berhasil mengambil data user")
        return {"message": "berhasil mengambil data user", "oldPassword" : result},200
        
    except Exception as e:
        logger.error(f"Terjadi error saat proses: {str(e)}")
        return {'message': 'Internal server error'}, 500

def userChangePasswordData(data):
    try:
        query = """
        UPDATE users
        SET password = %s
        WHERE id = %s
        """
        
        values = (data["newPassword"], data["user_id"])
        
        execute_query(query, values)
        
        logger.info("Berhasil mengubah data user")
        return {"message": "berhasil mengubah data user"},200
        
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500