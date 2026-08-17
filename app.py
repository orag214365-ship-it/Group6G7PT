from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Allows CodePen to send data to Python

DATA_FILE = "responses.json"

def read_responses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json or {}
    responses = read_responses()
    
    responses.append({
        "name": data.get("name", "Anonymous"),
        "favorite_part": data.get("favorite_part", "")
    })
    
    with open(DATA_FILE, "w") as f:
        json.dump(responses, f, indent=2)
        
    return jsonify({"status": "success"}), 200

@app.route('/responses', methods=['GET'])
def get_responses():
    return jsonify(read_responses())

if __name__ == '__main__':
    app.run(port=5000, debug=True)