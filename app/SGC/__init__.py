#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
from flask import Blueprint

sgc = Blueprint('sgc', __name__)

from . import views