from flask import Flask, request, jsonify
import jwt

from security.secret_key import SecretKeyAuth


app = Flask(__name__)


SECRET_KEY = SecretKeyAuth.get_secret_key()


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"Error": "No hay Token o es invalido"}), 400
        try:
            decoded_token = jwt.decode(token.split()[1], SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"Error": "El Token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"Error": "El Token es invalido"}), 401
        return f(*args, **kwargs)
    return wrapper


@app.route("/data-protected", methods=["GET"])
@token_required
def secure_data():
    return jsonify({"Acceso": "Pudo acceder con exito al back"})


if __name__ == "__main__":
    app.run(port=5001)