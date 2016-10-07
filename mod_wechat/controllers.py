# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, send_file, abort, url_for, current_app as app
from wechat.oauth2 import SCOPE_USERINFO
import msgpack
import qrcode
import StringIO

# 初始化蓝图
mod_wechat = Blueprint('wechat', __name__)


@mod_wechat.before_app_first_request
def first_request(*args, **kwargs):
    """初次请求处理"""
    # 如果没有定义回调地址，尝试增加回调地址    
    if app.wechat.client.defaults['redirect_uri'] is None:
        app.wechat.client.defaults['redirect_uri'] = url_for('wechat.callback', _external=True)


def qrcoder(state, userinfo=False):
    """生成二维码图片"""
    # 使用msgpack压缩请求参数
    state = msgpack.packb(state.to_dict()).encode('base64', 'strict')
    if userinfo:
        url = url_for('wechat.authorize', state=state, info='', _external=True)
    else:
        url = url_for('wechat.authorize', state=state, _external=True)
    print url
    img = qrcode.make(url)
    img_io = StringIO.StringIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@mod_wechat.route('/qr')
def qrcode_base():
    return qrcoder(request.args)


@mod_wechat.route('/qru')
def qrcode_userinfo():
    return qrcoder(request.args, userinfo=True)


@mod_wechat.route('/authz')
def authorize():
    """跳转至微信授权链接

    作用：
        直接二维码显示微信授权链接，可能长度过长导致生成失败，
        因此使用代理跳转来解决这个问题
    """
    print request.args['state']
    if 'state' in request.args:
        state = request.args['state']
    else:
        state = msgpack.packb(request.args.to_dict()).encode('base64', 'strict')
    if 'info' in request.args:
        url = app.wechat.client.get_authorize_url(state=state, scope=SCOPE_USERINFO)
    else:
        url = app.wechat.client.get_authorize_url(state=state)
    print url
    return redirect(url)


@mod_wechat.route('/cb')
def callback():
    """回调处理"""
    code = request.args['code']
    state = msgpack.unpackb(request.args['state'].decode('base64', 'strict'))
    print state
    workflow = state['wf'] if 'wf' in state else None
    print workflow
    # 判断用户是否授权
    if not app.wechat.client.is_authorized(request.args):
        reject_handler = app.wechat.user_reject_callback.get(workflow)
        if reject_handler is not None:
            return reject_handler(state)
        return abort(401)
    # 初始化处理上下文
    context = {'state': state}
    try:
        # 用户授权操作
        accept_handler = app.wechat.user_accept_callback.get(workflow)
        if accept_handler is not None:
            resp, context = accept_handler(context)
            if resp is not None:
                return resp
        # 获取授权令牌
        token = app.wechat.client.exchange_code(code=code)
        context['token'] = token
        access_token = token['access_token']
        # 忽略：
        #       expires_in = token['expires_in']
        #       refresh_token = token['refresh_token']
        openid = token['openid']
        scope = token['scope']
        # 判断是否需要获取用户信息授权
        is_user_info_required_handler = app.wechat.is_user_info_required_callback.get(workflow)
        if is_user_info_required_handler is not None:
            required, context = is_user_info_required_handler(context)
            print required
            if required:
                # 是否具有获取用户信息授权
                if scope == SCOPE_USERINFO:
                    # 是：获取并处理用户信息
                    user_info = app.wechat.client.get_user_info(access_token=access_token, openid=openid)
                    context['user_info'] = user_info
                    user_info_handler = app.wechat.user_info_callback.get(workflow)
                    if user_info_handler is not None:
                        context = user_info_handler(context)
                else:
                    # 否：重定向重新获取授权
                    return redirect(app.wechat.client.get_authorize_url(state=request.args['state'], scope=SCOPE_USERINFO))
        success_handler = app.wechat.success_callback.get(workflow)
        if success_handler is not None:
            return success_handler(context)
        else:
            return redirect(url_for('index'))
    except Exception, err:
        error_handler = app.wechat.error_callback.get(workflow)
        if error_handler is not None:
            return error_handler(err, context)
        else:
            return abort(500)


