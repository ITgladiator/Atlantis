#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")