import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from run import App

import sys
sys.path.append("../")
from CriticalFlowPath.config.paths import UPLD_FOLDER

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
os.makedirs(UPLD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "online"}), 200

######## curl X GET [API endpoint] ########

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload-xlsx-table', methods=['POST'])
def upload_xlsx_table_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only .xlsx and .xls allowed."}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLD_FOLDER, filename)
    file.save(file_path)

    # Trigger your model here if needed
    return jsonify({"message": "File uploaded successfully", "path": file_path}), 200

@app.route("/api/run", methods=["POST"])
def run_project():
    try:
        payload = request.get_json()
        result = App.main(payload)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
