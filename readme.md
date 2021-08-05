[回到首页](http://longtao.fun)
[项目列表](http://longtao.fun/product/product.html)

### 简单介绍

服务端代码,使用flask提供api服务，两个接口，一个用来上传，一个用来查看图片，上传图片返回图片url

```python
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
```

客户端脚本

```python
import os
import argparse
import base64
import sys
import requests


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
```

#### todo

1. 使用go重写方便部署
2. 图片去重
3. 图片压缩

### 使用方法

#### 服务端

1.  下载本repo源码
2.  安装python3环境，安装
3.  修改main 中的ip地址为你的服务端公网ip，是遏制iptables开启5555端口;
4.  nohup python3 $repoPath/main.py &启动或者通过systemd启动

```shell
echo "[Unit]
Description=simple picture pool
   
[Service]
Type=simple
ExecStart=/usr/bin/python3 /root/pic_pool/picture_pool/main.py > /dev/null   2>&1
   
[Install]
WantedBy=multi-user.target " > /etc/systemd/system/spp.service
systemctl status spp
systemctl start spp
systemctl enable spp
```



#### 客户端

1.  在你的修改upload_script.py 中的ip为你搭建的服务端ip（默认的172.20.18.38是我在0.10搭建好的）；
2.  在你的markdown 编辑器按照以下操作文件->偏好设置->图像->custom上传服务，在命令里填写`python3 upload_script.py的绝对路径 -i 你的服务ip地址  -s` 例如`python3 /home/longtao/workspace/projects/picture_pool/upload_script.py -i 172.20.18.38 -s`
3.  选择插入图片时上传图片，勾选，本地和网络，点击验证上传服务，如下为成功验证

