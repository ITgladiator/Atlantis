#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
from . import gdo
from flask import request, render_template, redirect, url_for
from flask_login import logout_user, login_user, login_required, current_user
from ..models import User
from app import db
from datetime import datetime


@gdo.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('stargate.index'))
        print email
        print password
    return render_template('gdo/login.html')


@gdo.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('gdo/register.html')
    # data = request.get_json()
    # email = data.get('email')
    # password = data.get('password')
    email = request.form.get('email')
    password = request.form.get('password')
    if User.query.filter_by(email=email).first():
        return '该邮箱已被注册！'
    nickname = email.split('@')[0]
    register_time = datetime.now()
    user = User(email=email, nickname=nickname, password=password, register_time=register_time)
    db.session.add(user)
    db.session.commit()
    # 发送邮件
    # ...
    return redirect(url_for('stargate.index'))


@gdo.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('stargate.index'))


# 验证用户
@gdo.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('stargate.index'))
    if current_user.confirm(token):
        return '确认完毕！'
    else:
        return '不可用或已过期!'


# 拦截未验证的用户
#@gdo.before_app_request
def before_request():
    if current_user.is_authenticated() \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'gdo.' \
            and request.endpoint != 'static':
        return redirect(url_for('gdo.unconfirmed'))


@gdo.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('stargate.index'))
    return render_template('gdo/unconfirmed.html')


# 重新发送验证邮件
@gdo.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    # 发送邮件
    return redirect(url_for('stargate.index'))
