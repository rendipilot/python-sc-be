from flask import Flask, request, jsonify
from joblib import load
import os
import zipfile
import json
import pandas as pd

app = Flask(__name__)

# Tentukan folder untuk menyimpan file yang diunggah
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tentukan ekstensi file yang diperbolehkan
ALLOWED_EXTENSIONS = {'sb3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load('models/rm_model.joblib')
# model = load('models/gbm_model.joblib')

@app.route("/predict", methods=["POST"])

def predict():
    
    #get file project
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # Pastikan nama file tidak kosong
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Periksa apakah file memiliki ekstensi yang diizinkan
    if file and allowed_file(file.filename):
        # Simpan file dengan nama aman
        filename = file.filename
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(filepath)
        
        #extrat file project
        with zipfile.ZipFile(file, "r") as zip_ref:
            with zip_ref.open('project.json') as json_file:
                project_data = json.load(json_file)
        
        if "targets" in project_data:
            targets_data = project_data["targets"]
        
        sprite = len(targets_data)
        
        block_categories = {
            "motion": 0, 
            "looks": 0, 
            "sound": 0, 
            "events": 0, 
            "control": 0, 
            "operators": 0, 
            "variables": 0, 
            "myblocks": 0
        }
        
        total_blocks = 0
        
        for target in targets_data:
            for block_id, block in target.get("blocks", {}).items():
                
                if isinstance(block, list):
                    continue 

                opcode = block.get("opcode", "")
                
                
                if "motion" in opcode:
                    block_categories["motion"] += 1
                    total_blocks += 1
                elif "looks" in opcode:
                    block_categories["looks"] += 1
                    total_blocks += 1
                elif "sound" in opcode:
                    block_categories["sound"] += 1
                    total_blocks += 1
                elif "event" in opcode:
                    block_categories["events"] += 1
                    total_blocks += 1
                elif "control" in opcode:
                    block_categories["control"] += 1
                    total_blocks += 1
                elif "operator" in opcode:
                    block_categories["operators"] += 1
                    total_blocks += 1
                elif "data" in opcode:
                    block_categories["variables"] += 1
                    total_blocks += 1
                elif "procedures" in opcode:
                    block_categories["myblocks"] += 1
                    total_blocks += 1

        features = {
            "total_blocks" : total_blocks,
            "motion_ratio" : block_categories["motion"] /total_blocks if total_blocks else 0,
            "looks_ratio" : block_categories["looks"] /total_blocks if total_blocks else 0,
            "sound_ratio" : block_categories["sound"] /total_blocks if total_blocks else 0,
            "events_ratio" : block_categories["events"] /total_blocks if total_blocks else 0,
            "control_ratio" : block_categories["control"] /total_blocks if total_blocks else 0,
            "operators_ratio" : block_categories["operators"] /total_blocks if total_blocks else 0,
            "variables_ratio" : block_categories["variables"] /total_blocks if total_blocks else 0,
            "myblocks_ratio" : 1 if block_categories["myblocks"] > 0 else 0,
            "sprite" : sprite
        }
        
        input_model = pd.DataFrame([features])
        
        prediction_model = model.predict(input_model)
        
        output = {
            "level": prediction_model[0][0],
            "creativity": prediction_model[0][1],
            "logical": prediction_model[0][2],
            "complexity": prediction_model[0][3]
        }

        #analysis data with model machine learning
        
        # Mengembalikan respons sukses
        return jsonify({"message": "File uploaded successfully", "filename": filename, "data": output
                        , "sprite": sprite}), 200
    
    else:
        return jsonify({"error": "Invalid file format. Only .sb3 files are allowed."}), 400
    


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    app.run(debug=True)