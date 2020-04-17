#! usr/bin/env python3
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from ServicesKeys import *
import requests
import sys
import hashlib
import time
import json

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

# Canvas Route
@app.route('/Canvas')
#@auth.login_required
def getCanvas():
    # building url to send to canvas
    filename = request.args.get('file')
    reqstring = 'https://vt.instructure.com/api/v1/courses/%s/files/?search_term=%s&access_token=%s' % (104692, filename, canvastoken)
    r = requests.get(reqstring)
    # downloading file from canvas
    canjson = json.loads(r.text[1:-1])
    url = canjson['url']
    canobj = requests.get(url, allow_redirects=True).content
    f = open(filename, 'wb').write(canobj)
    return (r.text, r.status_code, r.headers.items())

# Marvel Route
@app.route('/Marvel')
def getMarvel():
    # building url to send to marvel
    storynum = request.args.get('story')
    ts = str(time.time())
    hash = hashlib.md5((ts + marvelprivkey + marvelpubkey).encode()).hexdigest()
    reqstring = 'http://gateway.marvel.com/v1/public/stories/{story}?apikey={apikey}&hash={hash}&ts={ts}'.format(story=storynum, apikey=marvelpubkey, hash=hash, ts=ts)
    r = requests.get(reqstring)
    f = open("Story" + str(storynum) + ".txt", 'w+')
    f.write(r.text)
    return (r.text, r.status_code, r.headers.items())

# Main function
if __name__ == '__main__':
    # standard port number for web services
    portnum = 8080

    # receive port number from command line
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-p':
            portnum = sys.argv[i+1]

    # start running the app
    app.run(host = 'localhost', port=portnum, debug=True)
