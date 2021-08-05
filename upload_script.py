#!/usr/bin/python3
# -- coding: utf-8 --
# @Author : longtao.wu
# @Email: eustancewu@gmail.com
import os
import argparse
import base64
import sys
import requests

# ip = '172.20.18.38'

if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', type=str, nargs='+', help="必须传入文件", required=True)
parser.add_argument('-i', '--ip', type=str, nargs=1, help="必须指定地址", required=True)
args = parser.parse_args()
image_list = args.source
url = 'http://{}:5555/eus/v1/photo'.format(args.ip[0])


def get_data(_img):
    if os.path.isfile(_img):
        with open(_img, "rb") as f:
            file = f.read()
            encode_f = base64.b64encode(file)
    else:
        file = requests.get(_img).content
        encode_f = base64.b64encode(file)
    return encode_f


if __name__ == '__main__':
    for img in image_list:
        req = requests.post(url=url, data=get_data(img))
        print("http://"+str(req.text))
