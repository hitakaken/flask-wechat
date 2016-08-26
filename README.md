# flask-wechat
微信公众号 Flask Blueprint模块

## 安装
```bash
$ pip install flask-wechat-auth
```

## 使用

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