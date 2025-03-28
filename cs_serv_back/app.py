from flask import Flask


app = Flask(__name__)


@app.route("/secure-data", methods=["GET"])
def secure_data():
    return jsonify({"message": "Access granted to secure data"})


if __name__ == "__main__":
    app.run(port=5001)