import os
import io
import json
import shutil
import zipfile
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS

import sys
sys.path.append("../")
from backend.src.run import App
from backend.config.paths import RSLTS_DIR, UPLD_FOLDER

app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
os.makedirs(UPLD_FOLDER, exist_ok=True)

######## curl X GET [API endpoint] ########

@app.route("/api/", methods=["GET"])
def health():
    return jsonify({"status": "online"}), 200

@app.route("/api/download-file/<path:file_name>", methods=["GET"])
def download(file_name):
    file_dir  = os.path.join(RSLTS_DIR, file_name)
    print("Downloading:", file_dir)
    
    if not os.path.exists(file_dir):
        return abort(404, description="Path not found")
    
    if not os.path.isfile(file_dir):
        return abort(404, description="Path given is not a file")

    return send_from_directory(directory=RSLTS_DIR, path=file_name, as_attachment=True)

@app.route("/api/download-folder/<path:folder_name>", methods=["GET"])
def download_zip(folder_name):
    folder_dir = os.path.join(RSLTS_DIR, folder_name)

    if not os.path.exists(folder_dir) or not os.path.isdir(folder_dir):
        return abort(404, description="Folder not found")
    
    if not os.path.isdir(folder_dir):
        return abort(404, description="Path given is not a folder")

    # Create in-memory zip file
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, start=folder_dir)
                zf.write(abs_path, arcname=rel_path)
    memory_file.seek(0)

    zip_name = f"{os.path.basename(folder_name)}.zip"
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=zip_name
    )

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
    file_path = payload.get("file_name")

    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"Invalid file path: {file_path}")

    if os.stat(file_path).st_size == 0:
        raise ValueError(f"Excel file is empty: {file_path}")

    processed_project_dict = App.main(payload)

    return processed_project_dict

def return_processed_file(file_path:str):
    return send_file(
        file_path,
        as_attachment=True,
        download_name=os.path.basename(file_path),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route("/api/upload-file", methods=["POST"])
def upload_file():
    try:
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            return jsonify({"error": "No file provided"}), 400

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"[{timestamp}]__{uploaded_file.filename}"
        save_path = os.path.join(UPLD_FOLDER, filename)

        uploaded_file.save(save_path)

        return jsonify({"message": "File uploaded successfully", "path": save_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/execute-cfa-cycle", methods=["POST"])
def execute_module_cycle():
    try:
        # Get file and config from request
        file = request.files.get("file")
        config_json = request.form.get("config")

        if not file or not config_json:
            return jsonify({"error": "Missing 'file' or 'config' in request"}), 400

        # Parse config JSON string to dict
        payload = json.loads(config_json)

        # Save uploaded Excel file
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        saved_name = f"[{timestamp}]__{original_filename}"
        saved_path = os.path.join(UPLD_FOLDER, saved_name)
        file.save(saved_path)

        # Validate uploaded file
        if not os.path.exists(saved_path):
            return jsonify({"error": f"File not saved: {saved_path}"}), 500

        if os.stat(saved_path).st_size == 0:
            return jsonify({"error": f"Uploaded file is empty: {saved_path}"}), 400

        print(f"[INFO] File saved to: {saved_path}")
        print(f"[INFO] Size: {os.stat(saved_path).st_size} bytes")

        # Modify Payload: Inject file path and handle workweek entries
        payload["file_name"] = saved_path
        payload.setdefault("file_roi", "Sheet1")
        payload.setdefault("auto", True)

        if "project_workweek_start" in payload:
            payload.setdefault(
                "project_workweek", 
                f"{payload["project_workweek_start"]}-{payload["project_workweek_finish"]}"
            )

        # Process file (this should write output to a known results folder)
        result_dict = process_file(payload)

        if isinstance(result_dict, dict):
            output_folder = result_dict["setup"]["output_file"]["path"]
        else:
            output_folder = result_dict

        if not output_folder or not os.path.isdir(output_folder):
            return jsonify({"error": "Invalid output folder"}), 500

        # Zip the processed output folder in-memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(output_folder):
                for f in files:
                    abs_file = os.path.join(root, f)
                    rel_file = os.path.relpath(abs_file, start=output_folder)
                    zf.write(abs_file, arcname=rel_file)
        memory_file.seek(0)

        zip_name = f"{output_folder}.zip"

        # Return the zip as a download
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_name
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
