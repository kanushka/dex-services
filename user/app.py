# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from flask import Flask, request, jsonify, make_response
from flask import request
from os import environ
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

import db

app = Flask(__name__)
app.config['APP_SECRET_KEY'] = environ.get('APP_SECRET_KEY')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(
                token, app.config['APP_SECRET_KEY'], algorithms=["HS256"])
            current_user = db.get_user(data['email'])['Items'][0]
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    return "Welcome to DexLK Service"


@app.route('/user/<string:email>')
@token_required
def get_user(email):
    return jsonify(db.get_user(email))


@app.route('/user', methods=['POST'])
def create_user():
    data = request.form
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    user = db.get_user(email)
    if user['Count'] == 0:
        response = db.create_user(email, generate_password_hash(password), name)
        #TODO: Validate response
        return make_response('Successfully user registered.', 201)
    else:
        return make_response('User already exists. Please Log in.', 202)


@app.route('/auth', methods=['POST'])
def auth():
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    users = db.get_full_user(auth.get('email'))

    if users['Count'] == 0:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    user = users['Items'][0]
    email = user['Email']['S']

    if check_password_hash(user['Password']['S'], auth.get('password')):
        token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['APP_SECRET_KEY'], algorithm="HS256")

        print(token)
        decodede = jwt.decode(
            token, app.config['APP_SECRET_KEY'], algorithms=["HS256"])
        print(decodede)

        return make_response(jsonify({
            'token': token,
            'email': email,
            'name': user['Name']['S'],
            'user_id': user['UserId']['S']
        }), 201)

    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# if __name__ == '__main__':
#     app.run()
