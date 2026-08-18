from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allows CodePen to send data to Python

BIN_ID = "6a82b67df5f4af5e291f599b"
API_KEY = "$2a$10$40VNzo3BDca1JIT0uhII8.PlQuXDIYiylTGGUikm3G6mgqTdnAK8O"

HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

def get_cloud_responses():
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200:
            return res.json().get("record", [])
        return []
    except Exception as e:
        print("Error reading from JSONBin:", e)
        return []

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json or {}
    responses = get_cloud_responses()
    
    responses.append({
        "name": data.get("name", "Anonymous"),
        "favorite_part": data.get("favorite_part", "")
    })
    
    # Save updated array back to JSONBin cloud
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    requests.put(url, json=responses, headers=HEADERS)
    
    return jsonify({"status": "success"}), 200

@app.route('/responses', methods=['GET'])
def get_responses():
    return jsonify(get_cloud_responses())

if __name__ == '__main__':
    app.run(port=5000)
