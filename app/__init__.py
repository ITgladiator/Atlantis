#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'gdo.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .SGC import sgc as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/sgc')

    from .StarGate import stargate as show_blueprint
    app.register_blueprint(show_blueprint)

    from .GDO import gdo as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/gdo')

    return app