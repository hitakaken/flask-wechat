# flask-wechat
微信公众号 Flask Blueprint模块

+ 通过扫描二维码登录第三方网站

## 安装
```bash
$ pip install pillow
$ pip install flask-wechat-auth
```

## 启动服务

新建`setting.py`

```python
WX_APPID = "{WX_APPID}"
WX_SECRET = "{WX_SECRET}"
WX_CALLBACK_URL = "http://{hostname}/{prefix}/cb"
```

新建`run.py`

```python
from flask import Flask
from mod_wechat import WeChat

app = Flask(__name__)
app.config.from_object('settings')
wechat = WeChat(app, url_prefix='/auth')
app.run()
```

启动

```bash
python run.py
```

## 扫描登录

(TODO)