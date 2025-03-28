from flask import Flask, request, jsonify
import jwt
import datetime
import uuid

app = Flask(__name__)

@app.route("/token", methods=["POST"])
def generate_token():
    auth = request.authorization
    if not auth or auth.username != "admin" or auth.password != "123456":
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"token": "token"})

if __name__ == "__main__":
    app.run(port=5000)