from flask import Flask, request, jsonify
import jwt
import datetime
import uuid
import secrets

from entity.models import User
from security.secret_key import SecretKeyAuth


SECRET_KEY = SecretKeyAuth.get_secret_key()

app = Flask(__name__)


@app.route('/token', methods=['POST'])
def generate_token():
    auth = request.authorization
    if not User.get_user(auth.username, auth.password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user': auth.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'jti': str(uuid.uuid4())
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(port=5000)