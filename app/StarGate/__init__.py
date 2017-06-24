#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
from flask import Blueprint

stargate = Blueprint('stargate', __name__)

from . import views, errors