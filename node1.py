from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Shared resource (file)
shared_file_path = "file.txt"

# Token status
has_token = False  # Node 1 starts with the token

# Quorum nodes for Node 1
quorum_nodes = ["http://localhost:5001", "http://localhost:5002"]


@app.route('/request_token', methods=['POST'])
def request_token():
    global has_token
    if has_token:
        return jsonify({"error": "Token already held"}), 403
    responses = []

    # Check with other nodes in the quorum
    for node in quorum_nodes:
        try:
            response = requests.post(f"{node}/token_status")
            responses.append(response.json())
        except requests.exceptions.RequestException:
            return jsonify({"error": "Node communication failed"}), 500

    # Determine if the token can be granted
    # Ensure all nodes in the quorum do not have the token and this node doesn't either
    if all(r.get("has_token") == False for r in responses) and not has_token:
        has_token = True
        return jsonify({"status": "granted"}), 200
    else:
        return jsonify({"status": "denied"}), 403


@app.route('/grant_token', methods=['POST'])
def grant_token():
    global has_token
    if has_token:
        return jsonify({"error": "Token already held"}), 403

    # Check with other nodes to see if any hold the token
    for node in quorum_nodes:
        response = requests.post(f"{node}/token_status")
        token_status = response.json().get("has_token")
        if token_status:
            return jsonify({"error": "Token held by another node"}), 403

    # If no other nodes have the token, grant it to this node
    has_token = True
    return jsonify({"status": "token_granted"}), 200


@app.route('/release_token', methods=['POST'])
def release_token():
    global has_token
    if has_token:
        has_token = False
        return jsonify({"status": "token_released"}), 200
    else:
        return jsonify({"error": "No token to release"}), 403


@app.route('/read_file', methods=['GET'])
def read_file():
    if has_token:
        with open(shared_file_path, "r") as f:
            content = f.read()
        return jsonify({"content": content}), 200
    else:
        return jsonify({"error": "No token"}), 403


@app.route('/write_file', methods=['POST'])
def write_file():
    if has_token:
        data = request.json.get("data", "")
        with open(shared_file_path, "w") as f:
            f.write(data + "\n")
        return jsonify({"status": "written"}), 200
    else:
        return jsonify({"error": "No token"}), 403


@app.route('/append_file', methods=['POST'])
def append_file():
    if has_token:
        data = request.json.get("data", "")
        with open(shared_file_path, "a") as f:
            f.write(data + "\n")
        return jsonify({"status": "written"}), 200
    else:
        return jsonify({"error": "No token"}), 403


@app.route('/token_status', methods=['POST'])
def token_status():
    return jsonify({"has_token": has_token}), 200


if __name__ == '__main__':
    app.run(port=5000)  # Port for Node 1
