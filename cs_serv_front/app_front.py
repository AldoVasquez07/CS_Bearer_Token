import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for, session
from security.secret_key import SecretKeyAuth


app = Flask(__name__)

SECRET_KEY = SecretKeyAuth.get_secret_key()  # Necesario para manejar sesiones

AUTH_SERVER = "http://127.0.0.1:5000/token"  # Servidor de autenticación
PRODUCTS_API = "http://127.0.0.1:5001/producto"  # API de productos


class Producto:
    def __init__(self, id, nombre, descripcion, precio, stock):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock


@app.route("/", methods=["GET", "POST"])
def home():
    """ Página de login que obtiene un token de autenticación """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        response = requests.post(AUTH_SERVER, auth=(username, password))

        if response.status_code == 200:
            token = response.json().get("token")
            session["token"] = token  # Guardamos el token en la sesión
            return redirect(url_for("dashboard"))  # Redirige al dashboard
        
        return jsonify({"error": "Credenciales inválidas"}), 401

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """ Página principal con el CRUD de productos """
    token = session.get("token")
    if not token:
        return redirect(url_for("home"))

    headers = {"Authorization": f"Bearer {token}"}

    # Obtener productos
    response = requests.get(PRODUCTS_API + "s", headers=headers)
    productos_json = response.json() if response.status_code == 200 else []
    
    productos = [Producto(p[0], p[1], p[2], float(p[3]), p[4]) for p in productos_json]

    # Si se envía un formulario
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "agregar":
            datos = {
                "nombre": request.form["nombre"],
                "descripcion": request.form["descripcion"],
                "precio": request.form["precio"],
                "stock": request.form["stock"],
            }
            requests.post(PRODUCTS_API, json=datos, headers=headers)
        
        elif action == "editar":
            producto_id = request.form["id"]
            datos = {
                "nombre": request.form["nombre"],
                "descripcion": request.form["descripcion"],
                "precio": request.form["precio"],
                "stock": request.form["stock"],
            }
            requests.put(f"{PRODUCTS_API}/{producto_id}", json=datos, headers=headers)

        elif action == "eliminar":
            producto_id = request.form["id"]
            requests.delete(f"{PRODUCTS_API}/{producto_id}", headers=headers)

        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", productos=productos)


if __name__ == '__main__':
    app.run(port=4000, debug=True)  # Corre en otro puerto diferente al auth
