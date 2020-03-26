from fastai import *
from fastai.vision import *
import fastai
import sys
from io import BytesIO
from typing import List, Dict, Union, ByteString, Any
import os
import flask
from flask import Flask
import requests
import torch
import json


app = Flask(__name__)
tmp = {}


def load_model(path=".", file="classifier.pkl"):
    learn = load_learner(path, file=file)
    return learn


def load_image_url(url: str) -> Image:
    response = requests.get(url)
    img = open_image(BytesIO(response.content))
    return img


def load_image_bytes(raw_bytes: ByteString) -> Image:
    img = open_image(BytesIO(raw_bytes))
    return img


def classifier_predict(img, n: int = 3) -> Dict[str, Union[str, List]]:
    model = load_model('models')
    pred_class, pred_idx, outputs = model.predict(img)
    pred_probs = outputs / sum(outputs)
    pred_probs = pred_probs.tolist()
    predictions = []
    for image_class, output, prob in zip(model.data.classes, outputs.tolist(), pred_probs):
        output = round(output, 1)
        prob = round(prob, 2)
        predictions.append(
            {"class": image_class.replace(
                "_", " "), "output": output, "prob": prob}
        )

    predictions = sorted(predictions, key=lambda x: x["output"], reverse=True)
    predictions = predictions[0:n]
    return {'checked': tmp["checked"], "signal": 1, "class": str(pred_class), "predictions": predictions}


def segmentation_predict(img) -> Dict[str, Union[str, List]]:
    model = load_model('models', file="segmentation.pkl")
    pred = model.predict(img)[0]
    img.resize((3, 360, 480)).show(y=pred, figsize=(480/50, 360/50))
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)
    plt.savefig('tmp.png', dpi=100)
    import base64
    with open('tmp.png', 'rb') as img_f:
        img_stream = base64.b64encode(img_f.read()).decode()
    return {'checked': tmp["checked"], "signal": 2, "img_stream":img_stream}


def acc_camvid(input, target):
    target = target.squeeze(1)
    mask = target != void_code
    return (input.argmax(dim=1)[mask] == target[mask]).float().mean()


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
        return flask.jsonify(res)
    else:
        res = segmentation_predict(img)
        return res


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
        # app.run(host='0.0.0.0', port=port)
