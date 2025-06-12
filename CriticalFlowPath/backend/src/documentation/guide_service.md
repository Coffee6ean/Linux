# 🧭 **CriticalFlowPath Service – Developer Guide**

This document provides a **comprehensive guide** for developers to understand, use, and integrate with the `CriticalFlowPath` service. It covers setup, payload structure, and the execution flow via API calls.

---

## 🛠️ Setup Instructions

### ✅ 1. Environment Prerequisites

* Python 3.8+
* Flask (running locally or on EC2)
* PostgreSQL (if applicable)
* Optional: Gunicorn + Nginx for production deployment

### ✅ 2. Running the Flask Server

Navigate to your project directory and run the service:

```bash
python src/app.py
```

> ⚠️ Ensure `src/app.py` contains your Flask app and is properly configured to run on `host='0.0.0.0'` for remote access.

---

## 📂 Project Structure (Typical)

```plaintext
CriticalFlowPath/
├── src/
│   ├── app.py                  # Flask entry point
│   ├── run.py                  # Main execution logic
│   ├── modules/
│   │   ├── setup.py            # Project setup/configuration
│   │   ├── processor.py        # File logic
│   │   └── ...
└── README.md
```

---

## 🔁 Execution Flow

1. **Client uploads an Excel file** (`.xlsx`)
2. **Server parses the file** and generates a compatible `.json`
3. **Client sends a `.json` configuration** via a second request
4. **Server processes it**, initializes DB, and returns results or status

---

## 📥 API Endpoints & Usage

### **1. Upload `.xlsx` Table File**

**Endpoint**:

```
POST /api/upload-xlsx-table
```

**Form Data**:

| Key  | Type | Description          |
| ---- | ---- | -------------------- |
| file | file | Excel file to upload |

**Example (Linux)**:

```bash
curl -X POST http://<HOST>:5000/api/upload-xlsx-table -F "file=@/path/to/file.xlsx"
```

**Example (Git Bash)**:

```bash
curl -X POST http://127.0.0.1:5000/api/upload-xlsx-table -F "file=@/c/Users/your_username/Downloads/your_file.xlsx"
```

---

### **2. Run Project with `.json` Payload**

**Endpoint**:

```
POST /api/run
```

**Headers**:

```
Content-Type: application/json
```

**Payload**:
Send a JSON configuration like:

```json
{
  "setup": {
    "project": "Folsom Mall",
    "phase": "Phase 1",
    "trade": "Electrical"
  },
  "config": {
    "options": ["auto", "strict"]
  }
}
```

**Example**:

```bash
curl -X POST http://<HOST>:5000/api/run \
     -H "Content-Type: application/json" \
     -d @/path/to/config.json
```

---

## ☁️ Remote Usage (EC2 Integration)

### Copy Files to EC2:

```bash
scp -i /path/to/key.pem /local/file.xlsx ubuntu@<EC2_PUBLIC_DNS>:~/upload/
```

### Then from EC2 (or remote client):

```bash
curl -X POST http://127.0.0.1:5000/api/upload-xlsx-table -F "file=@/home/ubuntu/upload/file.xlsx"
```

---

## 📦 Payload & Response Structure

### Upload `.xlsx` Response:

```json
{
  "message": "File uploaded successfully.",
  "filename": "processed_file.xlsx",
  "path": "/tmp/processed_file.xlsx"
}
```

### Run `.json` Response:

```json
{
  "status": "success",
  "result": "Project executed successfully",
  "output_path": "/output/folder/result.json"
}
```

---

## 🔐 Best Practices for Security

* Store credentials in `.env` or `.secrets/`, never hardcoded.
* Enable CORS if the API is to be consumed by frontend clients.
* Use HTTPS (with Let's Encrypt or Cloudflare) for public-facing deployments.
* Validate all uploaded files and sanitize paths.

---

## 🤝 For Integrators

* Use multipart/form-data for file uploads
* Always check for success in the upload response before triggering `/api/run`
* Consider writing a wrapper script or Postman collection for testing
