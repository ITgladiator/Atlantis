#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
import hashlib
from flask import jsonify, request, render_template, redirect, url_for
from flask_login import current_user, login_required
import os
import time
import datetime

from app import db

from ..Ancients.ImageResize import imageResize
from ..Ancients.generate import generate

from config import BASE_DIR, INDEX_DIR, IMG_BASE_DIR
from ..models import *
from ..Ancients.SearchHelper import SearchHelper
from ..Ancients.jsonextend import CJsonEncoder
import json

from . import sgc
from ..Ancients.decorators import admin_required, permission_required


@sgc.route('/')
@login_required
def index():
    return render_template('sgc/index.html', username=current_user.email)


@sgc.route('/articles')
@login_required
def articles():
    return render_template('sgc/tables.html', username=current_user.email)


@sgc.route('/labels')
@login_required
def labels():
    return render_template('sgc/labels.html', username=current_user.email)

@sgc.route('/articleeditor')
@login_required
def addArticle():
    return render_template('/sgc/add_article.html', username=current_user.email)


@sgc.route('/articlecount', methods=['GET'])
@login_required
def articlecount():
    if current_user.is_administrator:
        article_count = Article.query.filter_by(delete_flag=False).count()
    else:
        article_count = Article.query.filter_by(delete_flag=False).filter_by(author_id=current_user.id).count()
    return str(article_count)


@sgc.route('/article', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def article():
    if request.method == 'GET':
        response_data = []
        page = request.args.get('page', 0, type=int)
        step = 20
        if current_user.is_administrator:
            pageination = Article.query.filter_by(delete_flag=False).order_by(Article.create_time.desc()).\
                paginate(page, step)
        else:
            pageination = Article.query.filter_by(delete_flage=False).filter_by(author_id=current_user.id).\
                order_by(Article.create_time.desc()).paginate(page, step)
        if not pageination.items:
            return jsonify(response_data)
        for art in pageination.items:
            author = art.author.nickname
            label = art.label.labelname
            response_data.append(dict(aid=art.id, title=art.title, label=label, author=author,
                                      create_time=art.create_time))
        return json.dumps(response_data, cls=CJsonEncoder)

    if request.method == 'POST':
        new_article = Article()
        new_article.title = request.form.get('title')
        new_article.body = request.form.get('content')
        new_article.summary = new_article.body[:240]
        new_article.label_id = request.form.get('label')
        new_article.create_time = datetime.datetime.now()
        new_article.modify_time = new_article.create_time
        new_article.author_id = current_user.id
        db.session.add(new_article)
        db.session.commit()
        # 异步添加搜索索引
        # ...
        return redirect(url_for('sgc.articles'))

    if request.method == 'DELETE':
        article_id = request.form.get('article_id')
        article = Article.query.filter_by(id=article_id).first()
        if article:
            article.delete_flag = True
            db.session.add(article)
            db.session.commit()
            return 'ok'
        else:
            return '未找到'


@sgc.route('/label', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def label():
    if request.method == 'GET':
        response_data = []
        labels = Label.query.all()
        for l in labels:
            article_count = Article.query.filter_by(label_id=l.id).count()
            response_data.append(dict(id=l.id, label_name=l.labelname, article_count=article_count))
        return jsonify(response_data)

    if request.method == 'POST':
        labelname = request.form.get('labelname')
        if len(labelname.strip()) == 0:
            return 'error'
        check_label = Label.query.filter_by(labelname=labelname).all()
        if check_label:
            return '类型已存在'
        label = Label()
        label.labelname = labelname
        db.session.add(label)
        db.session.commit()
        return 'ok'

    if request.method == 'PUT':
        labelid = request.form.get('labelid')
        labelname = request.form.get('labelname')
        label = Label.query.filter_by(id=labelid).first()
        if label:
            label.labelname = labelname
            return 'ok'
        else:
            return '未找到该分组'

    if request.method == 'DELETE':
        labelid = request.form.get('labelid')
        article_count = Article.query.filter_by(label_id=labelid).count()
        if article_count != 0:
            return '请先将文章从分类中移除', 400

        label = Label.query.filter_by(id=labelid).first()
        if label:
            db.session.delete(label)
            db.session.commit()
            return 'ok'
        else:
            return '未找到该分组', 404


@sgc.route('/multidelete')
@login_required
def multidelete():
    ids = request.get_json()
    # print ids
    # ids = json.loads(ids)
    for id in ids:
        article = Article.query.filter_by(id=id).first()
        if article:
            article.delete_flag = True
            db.session.add(article)
        else:
            return '未找到可删除的文章'
    db.session.commit()
    return '删除成功'
