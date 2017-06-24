#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^
from flask import jsonify, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..models import Article, Comment, User
from app import db
from . import stargate
import json
from ..Ancients.jsonextend import CJsonEncoder
from flask_login import login_required
import math
from datetime import datetime


@stargate.route('/')
def index():
    return render_template('stargate/index.html')


@stargate.route('/article')
def article():
    article_id = request.form.get('article_id')
    response_data = []
    article = Article.quer.filter_by(id=article_id).filter_by(delete_flag=False).first()
    if article:
        author = article.author.email
        label = article.label.labelname
        response_data.append(dict(id=article.id, title=article.title, summary=article.summary, content=article.body,
                                  create_time=article.create_time, author=author, label=label))
        # print "===============> ", article.image_path
    return json.dumps(response_data, cls=CJsonEncoder)


@stargate.route('/art_count')
def artcount():
    article_count = int(math.ceil(Article.query.filter_by(delete_flag=False).count() / 10.0))
    return str(article_count)


@stargate.route('/default')
def artdefult():
    response_data = []
    page = request.args.get('page', 0, type=int)
    step = 10
    offset = 0 if int(page) <= 0 else (int(page) - 1) * step
    articles = Article.query.filter_by(delete_flag=False).order_by(Article.create_time.desc()).offset(
        offset).limit(step).all()
    for art in articles:
        author = art.author.email
        label = art.label.labelname
        response_data.append(dict(id=art.id, title=art.title, label=label, author=author, summary=art.summary,
                                  create_time=art.create_time))
    return json.dumps(response_data, cls=CJsonEncoder)


@stargate.route('/details')
def details():
    article_id = request.args.get('article_id')
    article = Article.query.filter_by(id=article_id).filter_by(delete_flag=False).first()
    if article:
        author = article.author.email
        label = article.label.labelname
        content = article.body.split('\n')
        article.count += 1
        db.session.commit()
        return render_template('stargate/details.html', author=author, labelname=label, art_id=article_id,
                               create_time=article.create_time, content=content, title=article.title)
    else:
        return redirect(url_for('stargate.index'))


@stargate.route('/hotart')
def hotart():
    response_data = []
    count = request.args.get('count')
    articles = Article.query.filter_by(delete_flag=False).order_by(db.desc(Article.count)).offset(0).limit(count).all()
    for art in articles:
        response_data.append(dict(id=art.id, title=art.title))
    return jsonify(response_data)


@stargate.route('/comment', methods=['GET'])
def get_comment():
    response_data = []
    article_id = request.args.get('art_id')
    page = request.args.get('page', 0, type=int)
    step = 10
    offset = 0 if int(page) <= 0 else (int(page) - 1) * step
    comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.create_time.desc()). \
        offset(offset).limit(step).all()
    if comments:
        for comment in comments:
            # user = db.session.query(User.portrait).filter_by(username=comment.commentor).first()
            # if user:
            #     portrait = user.portrait
            # else:
            #     portrait = '/static/images/users/atlantis.png'
            response_data.append(dict(content=comment.content, create_time=comment.create_time,
                                      commentor=comment.commentor))
    return json.dumps(response_data, cls=CJsonEncoder)


@stargate.route('/comment', methods=['POST'])
@login_required
def post_comment():
    comments = json.loads(request.get_data())
    article_id = comments.get('art_id')
    content = comments.get('content')
    commentor = current_user.email
    comment = Comment()
    if commentor:
        comment.commentor = commentor
    comment.create_time = datetime.now()
    comment.content = content
    comment.article_id = article_id
    db.session.add(comment)
    db.session.commit()
    return 'ok'


@stargate.route('/commentcount')
def commentCount():
    article_id = request.args.get('art_id')
    count = Comment.query.filter_by(article_id=article_id).count()
    return str(count)