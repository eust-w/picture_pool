#!/usr/bin/python3
# -- coding: utf-8 --
# @Author : longtao.wu
# @Email: eustancewu@gmail.com

import base64
import os
import uuid

from flask import Flask, request, make_response

ip = '127.0.0.1'

file_path = os.path.join(os.path.dirname(__file__), 'pics')
app = Flask(__name__)


@app.route("/eus/v1/photo", methods=['POST'])
def get_frame():
    upload_file = request.data
    img = base64.b64decode(upload_file)
    file_name = str(uuid.uuid1())
    file_paths = os.path.join(file_path, file_name)
    with open(file_paths, "wb") as f:
        f.write(img)
        return 'http://{}:5555/eus/v1/show/{}'.format(ip, file_name)


@app.route("/eus/v1/show/<string:filename>", methods=['GET'])
def show(filename):
    file_paths = os.path.join(file_path, filename)
    f = open(file_paths, "rb").read()
    response = make_response(f)
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5555)
