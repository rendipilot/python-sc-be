from db import execute_query
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def convert_data(data):
    # Mengonversi semua nilai menjadi float untuk memastikan tipe data yang benar
    return {
        "creativity": float(data.get("creativity", 0)),
        "logical": float(data.get("logical", 0)),
        "complexity": float(data.get("complexity", 0)),
        "level": float(data.get("level", 0))
    }

def predictData(filename, data, user_id):
    
    data = convert_data(data)
    try:
        query = """
        INSERT INTO histories
        (name, user_id, creativity_score, logical_score, complexity_score, level_score, created_at)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            filename,
            user_id,
            data["creativity"],
            data["logical"],
            data["complexity"],
            data["level"],
            datetime.now()
        )
        
        execute_query(query, values)
        
        logger.info(f"Berhasil mengirimkan data : {filename}")
        return {'message': 'berhasil mengirimkan data','filename': filename, "data": data}, 200
                
    except Exception as e:
        logger.error(f"Terjadi error saat login: {str(e)}")
        return {'message': 'Internal server error'}, 500    