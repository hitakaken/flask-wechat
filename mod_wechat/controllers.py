# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, send_file, abort
from wechat.client import WechatAPI
from wechat.oauth2 import SCOPE_USERINFO
import msgpack
import qrcode
import StringIO

# 初始化蓝图
mod_wechat = Blueprint('wechat', __name__)

# 定义全局变量
client = None
url_for = None


@mod_wechat.record
def init_mod(setup_state):
    """初始化超链接生成器和微信开发客户端"""
    global client, url_for
    app = setup_state.app
    if hasattr(app, 'url_for'):
        url_for = app.url_for
    else:
        from flask import url_for as flask_url_for
        url_for = flask_url_for
    if 'WX_CALLBACK_URL' in app.config:
        redirect_uri = app.config['WX_CALLBACK_URL']
    else:
        redirect_uri = None

    client = WechatAPI(
        appid=app.config['WX_APPID'],
        secret=app.config['WX_SECRET'],
        redirect_uri=redirect_uri
    )
    setattr(app, 'wechat_client', client)
    setattr(mod_wechat, 'client',client)


@mod_wechat.before_app_first_request
def first_request(*args, **kwargs):
    """初次请求处理"""
    # 如果没有定义回调地址，尝试增加回调地址
    if client.defaults['redirect_uri'] is None:
        client.defaults['redirect_uri'] = url_for('wechat.callback', _external=True)


@mod_wechat.route('/qr')
def qrcoder():
    """生成二维码图片"""
    state = msgpack.packb(dict(request.args)).encode('base64', 'strict')
    url = url_for('wechat.authorize', state=state, _external=True)
    img = qrcode.make(url)
    img_io = StringIO.StringIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@mod_wechat.route('/authz')
def authorize():
    """跳转至微信授权链接"""
    if 'info' in request.args:
        print client.get_authorize_url(state=request.args['state'], scope=SCOPE_USERINFO)
    print client.get_authorize_url(state=request.args['state'])
    return abort(404)


@mod_wechat.route('/cb')
def callback():
    if not client.is_authorized(request.args):
        return abort(401)

