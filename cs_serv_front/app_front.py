import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for

app = Flask(__name__)

AUTH_SERVER = "http://127.0.0.1:5000/token"  # URL del servidor de autenticación

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        response = requests.post(AUTH_SERVER, auth=(username, password))
        
        if response.status_code == 200:
            return redirect(url_for("dashboard"))  # Redirige a la nueva página
        
        return jsonify({"error": "Credenciales inválidas"}), 401

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")  # Nueva página después del login

if __name__ == '__main__':
    app.run(port=4000, debug=True)  # Corre en otro puerto diferente al auth
