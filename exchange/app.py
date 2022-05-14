# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

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
    return "Welcome to Exchage Service"


@app.route('/exchange', methods=['POST'])
@token_required
def exchange():
    address = request.form["wallet"]
    from_currency = request.form["from_currency"]
    from_amount = request.form["amount"]
    to_currency = request.form["to_currency"]

    rate = util.get_exchange_rate(from_currency, to_currency)
    to_amount = float(from_amount) * rate

    return jsonify(db.exchange(address, from_currency, from_amount, to_currency, str(to_amount)))


if __name__ == '__main__':
    app.run()
