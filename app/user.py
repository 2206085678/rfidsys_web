import functools
from flask import (
    render_template, flash, redirect, Blueprint,
    g, redirect, request, session, url_for)
from werkzeug.security import check_password_hash,generate_password_hash
from app.db import get_db

bp = Blueprint("user",__name__,url_prefix="/user")


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    注册用户视图
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('user.login'))

        flash(error)

    return render_template('user/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    登录视图
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '请输入用户名'
        elif not check_password_hash(user['password'], password):
            error = '密码错误'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('user/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    ？？？
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    """
    注销
    """
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    装饰器
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view