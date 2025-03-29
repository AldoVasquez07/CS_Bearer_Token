from flask import Flask, request, jsonify
import jwt

from security.secret_key import SecretKeyAuth
from entity.models import Productos

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

@app.route("/productos", methods=["GET"])
@token_required
def obtener_productos():
    """ Devuelve todos los productos con estado True. """
    productos = Productos.get_productos()
    return jsonify(productos)


@app.route("/producto/<int:id>", methods=["GET"])
@token_required
def obtener_producto(id):
    """ Devuelve un producto por ID si está activo. """
    producto = Productos.get_producto(id)
    if producto:
        return jsonify(producto)
    return jsonify({"Error": "Producto no encontrado"}), 404


@app.route("/producto/<int:id>", methods=["DELETE"])
@token_required
def eliminar_producto(id):
    """ Cambia el estado de un producto a False en lugar de eliminarlo. """
    resultado = Productos.delete_producto(id)
    if resultado:
        return jsonify({"Mensaje": "Producto desactivado correctamente"})
    return jsonify({"Error": "No se pudo desactivar el producto"}), 500


@app.route("/producto", methods=["POST"])
@token_required
def agregar_producto():
    """ Agrega un nuevo producto con estado True. """
    datos = request.get_json()
    if not all(k in datos for k in ["nombre", "descripcion", "precio", "stock"]):
        return jsonify({"Error": "Faltan datos"}), 400

    nuevo_id = Productos.insert_producto(datos["nombre"], datos["descripcion"], datos["precio"], datos["stock"])
    if nuevo_id:
        return jsonify({"Mensaje": "Producto agregado con éxito", "id": nuevo_id})
    return jsonify({"Error": "No se pudo agregar el producto"}), 500


if __name__ == "__main__":
    app.run(port=5001)