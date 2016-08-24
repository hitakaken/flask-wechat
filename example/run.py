# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
app.config.from_object('settings')
from mod_wechat import WeChat
wechat = WeChat(app, url_prefix='/auth')

app.run(debug=True)
