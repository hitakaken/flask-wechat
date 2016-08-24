# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
app.config.from_object('settings')
from mod_wechat import WeChat
WeChat(app)

app.run(debug=True)
