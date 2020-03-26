from fastai.vision import *
import fastai
import sys
from io import BytesIO
import os
import flask
from flask import Flask
import json
from predict import *

app = Flask(__name__)
tmp = {}

@app.route('/_predict', methods=['POST', 'GET'])
def upload_file():
    if flask.request.method == 'GET':
        url = flask.request.args.get("url")
        img = load_image_url(url)
    else:
        bytes = flask.request.files['file'].read()
        img = load_image_bytes(bytes)
    if tmp["checked"] == "classifier":
        res = classifier_predict(img)
    else:
        res = segmentation_predict(img)
    res['checked']=str(tmp["checked"])
    return flask.jsonify(res)


@app.route('/_checked', methods=['GET'])
def check():
    tmp["checked"] = flask.request.args.get("checked").replace(" ", "")
    return tmp["checked"]

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    response.cache_control.max_age = 0
    return response


@app.route('/<path:path>')
def static_file(path):
    if ".js" in path or ".css" in path:
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')


@app.route('/')
def root():
    return app.send_static_file('index.html')


def before_request():
    app.jinja_env.cache = {}


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)

    if "prepare" not in sys.argv:
        app.jinja_env.auto_reload = True
        app.run(debug=True, host='0.0.0.0', port=port)
