from flask import Flask, request, jsonify
import jwt
import datetime
import uuid
import secrets


app = Flask(__name__)


def get_secret_key():
    with open('../sec_workspace/SECRET_KEY.txt', 'r') as file:
        return file.read().strip()


def get_user(username, password):
    with open("../bd_simulation/users.txt", "r") as users:
        for user in users:
            stored_username, stored_password = user.strip().split("|")
            if stored_username == username and stored_password == password:
                return True
    return False


SECRET_KEY = get_secret_key()


@app.route('/token', methods=['POST'])
def generate_token():
    auth = request.authorization
    if not get_user(auth.username, auth.password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user': auth.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'jti': str(uuid.uuid4())
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(port=5000)