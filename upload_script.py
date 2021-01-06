#!/usr/bin/python3
# -- coding: utf-8 --
# @Author : longtao.wu
# @Email: eustancewu@gmail.com
import argparse
import base64
import sys
import requests
import json

ip = '172.20.18.38'

url = 'http://{}:5555/eus/v1/photo'.format(ip)
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', type=str, nargs='+', help="必须传入文件", required=True)
args = parser.parse_args()
image_list = args.source


def get_data(_img):
    with open(_img, "rb") as f:
        file = f.read()
        encode_f = base64.b64encode(file)
    return encode_f


if __name__ == '__main__':
    for img in image_list:
        data = get_data(img)
        req = requests.post(url=url, data=data)
        print(str(req.text))
