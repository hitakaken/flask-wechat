# -*- coding: utf-8 -*-
from flask import Flask, abort, url_for as flask_url_for, jsonify, redirect

app = Flask(__name__)
app.config.from_object('settings')
redirect_url_prefix = 'http://test.qbxh.sh.cn'


def url_for(endpoint, **values):
    if redirect_url_prefix is None:
        return flask_url_for(endpoint, **values)
    else:
        if '_external' in values:
            del values['_external']
        return redirect_url_prefix + flask_url_for(endpoint, **values)

setattr(app, 'url_for', url_for)

from mod_wechat import WeChat

wechat = WeChat(app, url_prefix='/auth')


@wechat.user_reject('login')
def user_reject(ctx):
    state = ctx['state']
    # TODO 用户拒绝处理
    return abort(401)


@wechat.user_accept('login')
def user_accept(ctx):
    state = ctx['state']
    # TODO 根据状态判断是否可以直接返回
    return None, ctx


@wechat.is_user_info_required('login')
def is_user_info_required(ctx):
    token = ctx['token']
    openid = token['openid']
    # TODO 检查用户是否已经存在
    return True, ctx


@wechat.user_info('login')
def handle_user_info(ctx):
    user_info = ctx['user_info']
    # TODO 将用户存入数据库
    return ctx


@wechat.success('login')
def success(ctx):
    # TODO 授权成功的操作
    return redirect(url_for('index'))


@wechat.error('login')
def error(err, ctx):
    # TODO 授权失败的操作
    return abort(500)


@app.route('/')
def index():
    return jsonify({'hello': 'world'})


app.run(host='0.0.0.0', debug=True)
