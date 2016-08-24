# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


mod_wechat = Blueprint('wechat', __name__, url_prefix='/wechat', static_folder='static', template_folder='templates')


@mod_wechat.route('/login')
def login():
    return render_template('login.html', authorize_url_prefix=url_for('wechat.authorize', client=''))