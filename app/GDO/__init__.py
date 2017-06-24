#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
from flask import Blueprint

gdo = Blueprint('gdo', __name__)

from . import views