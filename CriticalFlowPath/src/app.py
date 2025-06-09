import os
import json
import shutil
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from run import App

import sys
sys.path.append("../")
from CriticalFlowPath.config.paths import UPLD_FOLDER

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
os.makedirs(UPLD_FOLDER, exist_ok=True)

######## curl X GET [API endpoint] ########

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "online"}), 200

######## curl X POST [API endpoint] ########

def allowed_file(filename:str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file_path:str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    filename = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    saved_name = f"[{timestamp}]__{filename}"
    save_path = os.path.join(UPLD_FOLDER, saved_name)

    shutil.copy(file_path, save_path)
    return save_path

def process_file(payload:dict) -> dict:
    processed_project_dict = App.main(payload)

    return processed_project_dict

def return_processed_file(file_path:str):
    return send_file(
        file_path,
        as_attachment=True,
        download_name=os.path.basename(file_path),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# === FINAL API ENTRY POINT ===
@app.route("/api/execute-cfa-cycle", methods=["POST"])
def execute_module_cycle():
    try:
        # Step 1: Upload file
        if "file" not in request.files:
            return jsonify({"error": "No file part in request"}), 400
        
        file = request.files["file"]

        # Step 2: Read and parse JSON
        try:
            payload = json.loads(file.read().decode("utf-8"))
        except Exception:
            return jsonify({"error": "Invalid JSON format"}), 400

        target_path = payload["file_name"]
        uploaded_path = save_uploaded_file(target_path)
        payload["file_name"] = uploaded_path

        # Step 2: Process file
        processed_path = process_file(payload)

        # Step 3: Return file
        return return_processed_file(processed_path)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
