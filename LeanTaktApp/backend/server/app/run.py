from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/process', methods=['POST'])
def process_file():
    try:
        data = request.get_json()
        print("Received data:", data)
        
        result = {"status": "success", "received_data": data}
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)