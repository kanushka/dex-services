# Author: Kanushka Gayan
# Student Id: MS21911262
# Created: 2022.05.08

from flask import Flask, jsonify
from flask import request
import db

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Auth Service"


@app.route('/user/<string:username>')
def get_user(username):
    return jsonify(db.get_user(username))


@app.route('/user', methods=['POST'])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    return jsonify(db.create_user(username, password))


@app.route('/auth', methods=['POST'])
def auth():
    username = request.form["username"]
    password = request.form["password"]
    return jsonify(db.check_password(username, password))


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=7007)
