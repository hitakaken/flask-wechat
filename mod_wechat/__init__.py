# -*- coding: utf-8 -*-


class SocketIO(object):
    def __init__(self, app=None, **kwargs):
        if app is not None or len(kwargs) > 0:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        from mod_wechat.controllers import mod_wechat as wechat_module
        app.register_blueprint(wechat_module)
