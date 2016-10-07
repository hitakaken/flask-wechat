# -*- coding: utf-8 -*-
from wechat.client import WechatAPI


class WeChat(object):
    def __init__(self, app=None, **kwargs):
        # 用户拒绝授权回调处理
        self.user_reject_callback = {}
        # 用户授权成功回调处理
        self.user_accept_callback = {}
        # 是否需要获取用户信息
        self.is_user_info_required_callback = {}
        # 获取用户信息回调处理
        self.user_info_callback = {}
        # 授权成功回调处理
        self.success_callback = {}
        # 授权失败回调处理
        self.error_callback = {}
        self.client = None
        if app is not None or len(kwargs) > 0:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        import mod_wechat.controllers
        from mod_wechat.controllers import mod_wechat as wechat_module
        setattr(wechat_module, 'wrapper', self)
        if not hasattr(app, 'url_for'):
            from flask import url_for as flask_url_for
            setattr(app, 'url_for', flask_url_for)
        if 'WX_CALLBACK_URL' in app.config:
            redirect_uri = app.config['WX_CALLBACK_URL']
        else:
            redirect_uri = None
        self.client = WechatAPI(
            appid=app.config['WX_APPID'],
            secret=app.config['WX_SECRET'],
            redirect_uri=redirect_uri
        )
        wechat_module.client = self.client
        setattr(app, 'wechat', self)

        app.register_blueprint(wechat_module, **kwargs)

    def user_reject(self, workflow=None):
        module = self

        def set_callback(callback):
            module.user_reject_callback.setdefault(workflow, callback)
        return set_callback

    def user_accept(self, workflow=None):
        module = self

        def set_callback(callback):
            module.user_accept_callback.setdefault(workflow, callback)
        return set_callback

    def is_user_info_required(self, workflow=None):
        module = self

        def set_callback(callback):
            module.is_user_info_required_callback.setdefault(workflow, callback)

        return set_callback

    def user_info(self, workflow=None):
        module = self

        def set_callback(callback):
            module.user_info_callback.setdefault(workflow, callback)

        return set_callback

    def success(self, workflow=None):
        module = self

        def set_callback(callback):
            module.success_callback.setdefault(workflow, callback)

        return set_callback

    def error(self, workflow=None):
        module = self

        def set_callback(callback):
            module.error_callback.setdefault(workflow, callback)

        return set_callback






