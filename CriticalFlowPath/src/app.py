from flask import Flask, request, jsonify
from run import App  # your main class

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "online"}), 200

@app.route("/api/run", methods=["POST"])
def run_project():
    try:
        payload = request.get_json()
        result = App.run_from_dict(payload)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
