# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, send_file
from wechat.client import WechatAPI
import qrcode
import pickle
import StringIO

# 初始化蓝图
mod_wechat = Blueprint('wechat', __name__)

# 定义全局变量
client = None
url_for = None


@mod_wechat.record
def get_url_for(setup_state):
    """初始化超链接生成器和微信开发客户端"""
    global wechat, url_for
    app = setup_state.app
    if hasattr(app, 'url_for'):
        url_for = app.url_for
    else:
        from flask import url_for as flask_url_for
        url_for = flask_url_for
    if 'WX_CALLBACK_URL' in app.config:
        redirect_uri = app.config['WX_CALLBACK_URL']
    elif 'SERVER_NAME' in app.config:
        redirect_uri = url_for('wechat.callback', _external=True)
    else:
        redirect_uri = None

    client = WechatAPI(
        appid=app.config['WX_APPID'],
        secret=app.config['WX_SECRET'],
        redirect_uri=redirect_uri
    )
    setattr(app, 'wechat_client', client)
    setattr(mod_wechat, 'client',client)


@mod_wechat.route('/qrcode')
def qrcode():
    state = pickle.dumps(request.args).encode('base64', 'strict')
    img = qrcode.make(url_for('wechat.proxy', state=state))
    img_io = StringIO()
    img.save(img_io)
    return send_file(img_io, mimetype='image/jpeg')


@mod_wechat.route('/authorize')
def proxy():
    return redirect(wechat.get_authorize_url(state=request.args['state']))

