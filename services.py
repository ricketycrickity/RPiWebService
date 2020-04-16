#! usr/bin/env python3
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from tokens import *
import sys

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    # standard port number for web services
    portnum = 8080

    # receive port number from command line
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-p':
            portnum = sys.argv[i+1]

    # start running the app
    app.run(host = 'localhost', port=portnum, debug=True)
