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
    return "Welcome to Exchage Service"


@app.route('/exchange', methods=['POST'])
def exchange():
    address = request.form["wallet"]
    from_currency = request.form["from_currency"]
    from_amount = request.form["amount"]
    to_currency = request.form["to_currency"]

    rate = util.get_exchange_rate(from_currency, to_currency)
    to_amount = float(from_amount) * rate

    return jsonify(db.exchange(address, from_currency, from_amount, to_currency, str(to_amount)))


# if __name__ == '__main__':
#     app.run()
