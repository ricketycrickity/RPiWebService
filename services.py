#! usr/bin/env python3
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from ServicesKeys import *
import requests
import sys

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "username": generate_password_hash("admin"),
    "password": generate_password_hash("secret")
}
"""
@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    print('>Could not verify your access level for that URL. You have to login with proper credentials')
    return False
"""
@app.route('/')
def basicReply():
    return "Hello!"


@app.route('/Canvas')
#@auth.login_required
def getCanvas():
    filename = request.args.get('file')
    return "<h1>Going to Canvas to find %s!</h1>" % filename

@app.route('/Marvel')
def getMarvel():
    storynum = request.args.get('story')
    return "<h1>Going to Marvel to find story #%s!</h1>" % storynum

if __name__ == '__main__':
    # standard port number for web services
    portnum = 8080

    # receive port number from command line
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-p':
            portnum = sys.argv[i+1]

    # start running the app
    app.run(host = 'localhost', port=portnum, debug=True)
