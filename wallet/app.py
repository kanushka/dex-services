# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from urllib import response
from flask import Flask, request, jsonify, make_response
from flask import request
from os import environ
import jwt
from functools import wraps


import db
import util

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
            print(token)
            data = jwt.decode(
                token, app.config['APP_SECRET_KEY'], algorithms=["HS256"])
            print(data)
            current_user = db.get_user(data['email'])['Items'][0]
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    return "Welcome to Wallet Service"


@app.route('/wallet/<uuid:user_id>')
@token_required
def get_wallet(user_id):
    return jsonify(db.get_wallet(user_id))


@app.route('/wallet', methods=['POST'])
@token_required
def create_wallet():
    user_id = request.form["user_id"]
    address = util.id_generator(64)
    response = db.create_wallet(user_id, address)
    # TODO: Validate response
    return make_response('Successfully wallet created.', 201)


@app.route('/wallet/funds', methods=['POST'])
@token_required
def add_funds():
    address = request.form["wallet"]
    currency = request.form["currency"]
    amount = request.form["amount"]
    return jsonify(db.add_funds(address, currency, amount))


# if __name__ == '__main__':
#     app.run()
