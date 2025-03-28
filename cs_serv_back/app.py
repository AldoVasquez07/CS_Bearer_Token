from flask import Flask
import jwt

app = Flask(__name__)

SECRET_KEY = "supersecretkey"


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token is missing or invalid"}), 400
        try:
            decoded_token = jwt.decode(token.split()[1], SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper


@app.route("/secure-data", methods=["GET"])
@token_required
def secure_data():
    return jsonify({"message": "Access granted to secure data"})


if __name__ == "__main__":
    app.run(port=5001)