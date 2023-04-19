from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, session)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT p.id, title, post_body, value, post_created, post_author_id, username'
        ' FROM post p JOIN user u ON p.post_author_id = u.id'
        ' ORDER BY post_created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods= ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['post_body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, post_body, post_author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, post_body, post_created, post_author_id, username'
        ' FROM post p JOIN user u ON p.post_author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['post_author_id'] != g.user['id']:
        abort(403)

    return post

def get_comment(id, check_author=True):
    comment = get_db().execute(
        'SELECT c.id, comment_body, comment_created, comment_author_id, post_id, username'
        ' FROM comment c JOIN user u ON c.comment_author_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if comment is None:
        abort(404, f"Comment id {id} doesn't exist.")

    if check_author and comment['comment_author_id'] != g.user['id']:
        abort(403)

    return comment

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['post_body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, post_body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/comment')
def comment(id):
    db = get_db()
    comments = db.execute('SELECT c.id, comment_body, comment_created, comment_author_id, post_id, username'
        ' FROM comment c JOIN user u ON c.comment_author_id = u.id'
        ' WHERE post_id = ?'
        ' ORDER BY comment_created DESC',
        (id,)
    ).fetchall()
    return render_template('blog/comment.html', comments=comments, post=id)

@bp.route('/<int:id>/addcomment', methods=('POST', 'GET'))
@login_required
def addcomment(id):
    user_id = session.get('user_id')

    if request.method == 'POST':
        body = request.form['comment_body']
        error = None

        if not comment:
            error = ('You have not entered a comment.')

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (comment_body, comment_author_id, post_id)'
                ' VALUES (?, ?, ?)',
                (body, user_id, id)
            )
            db.execute(
                'UPDATE post SET value = value + 1 WHERE id = ?',
                (id,)
            )
            db.commit()
            return redirect(url_for('blog.comment', id=id))
    return render_template('blog/addcomment.html', post=id)

@bp.route('/<int:id>/updatecomment', methods=('GET', 'POST'))
@login_required
def updatecomment(id):
    comment_acquired = get_comment(id)

    if request.method == 'POST':
        body = request.form['comment_body']
        error = None

        if not body:
            error = 'Comment is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE comment SET comment_body = ?'
                ' WHERE id = ?',
                (body, id)
            )
            db.commit()
            return redirect(url_for('blog.comment', id=comment_acquired['post_id']))

    return render_template('blog/updatecomment.html', comment=comment_acquired)

@bp.route('/<int:id>/deletecomment', methods=('POST',))
@login_required
def deletecomment(id):
    comment_acquired = get_comment(id)
    db = get_db()
    db.execute('DELETE FROM comment WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.comment', id=comment_acquired['post_id']))

@bp.route('/search', methods=['POST'])
def search():

    if request.method == 'POST':
        query = request.form['search_content']
        error = None

        if not query:
            error = 'You have not entered a relevant search.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            posts = db.execute('SELECT p.id, title, post_body, post_created, post_author_id, username'
                ' FROM post p JOIN user u ON p.post_author_id = u.id'
                ' WHERE (title LIKE ? OR post_body LIKE ? OR username LIKE ?)'
                ' ORDER BY post_created DESC',
                ('%' + query + '%', '%' + query + '%', '%' + query + '%')
            ).fetchall()
            return render_template('blog/search.html', posts=posts)
    return index()