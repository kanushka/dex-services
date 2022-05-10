# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from flask import Flask, jsonify
from flask import request
import db
import util

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Wallet Service"


@app.route('/wallet/<uuid:user_id>')
def get_wallet(user_id):
    return jsonify(db.get_wallet(user_id))


@app.route('/wallet', methods=['POST'])
def create_wallet():
    user_id = request.form["user_id"]
    address = util.id_generator(64)
    return jsonify(db.create_wallet(user_id, address))


@app.route('/wallet/funds', methods=['POST'])
def add_funds():
    address = request.form["wallet"]
    currency = request.form["currency"]
    amount = request.form["amount"]
    return jsonify(db.add_funds(address, currency, amount))


# if __name__ == '__main__':
#     app.run()
