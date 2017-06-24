#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMG_BASE_DIR = 'static/images/articles'
HTML_OUT_PATH = os.path.join(BASE_DIR, 'static/out')
INDEX_DIR = os.path.join(BASE_DIR, 'index')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ATLANTIS_ADMIN = "506226866@qq.com"

    MAIL_SERVER = ''

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://atlantis:123456@127.0.0.1/atlantisV2'


config = {
    'dev': DevelopmentConfig,
    'default': DevelopmentConfig,
}