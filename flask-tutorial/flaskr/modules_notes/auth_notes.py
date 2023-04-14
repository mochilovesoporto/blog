"""import functools
from flask import(Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# creates blueprint named 'auth', __name__ tells where defined,
bp = Blueprint('auth', __name__, url_prefix='/auth')

# register function runs before view function no matter URL requested
# load_logged_in_user checks if user id stored in session and gets user's data from database
# stores data in g.user (lasts length of request)
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

# user visits /auth/register URL, register view will return HTML w/ form to fill
# once submitted, it validates input and either show form again w/ error or create new user & go login in page
# bp.route associates URL register w/ register view function, when request recieved it calls register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST'
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                #db.execute takes SQL query w/ ? placeholders for any user input, & a tuple of value to replace placeholders
                # for security reasons passwords never stored in database directly,
                # instead generate_password_hash() used to securely hash the password & hash is stored
                # db commit must be called afterwards as data has been changed (need save changes)
                db.execute(
                    "INSERT INTO user (username,password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            # integrity error occur if name already exists
            except db.IntegrityError:
                error = f'User{username} is already registered.'
            # after storing user, redirected by url_for to login
            else:
                return redirect(url_for('auth.login'))

        # if validation fails, error is show to user, flash() stores messages that can be retrieved when rendering temp.
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.methods == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # User queried first & stored in variable for later use
        # fetchone() returns one row form query, if query returns no result, it returns none
        # determines if user exists based on username
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Incorrect username.'
        # checks stored password hash against entered password hash for match
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # session is dict stores data across requests
        # when validation is success, users id stored in a new session
        # data is stored in a cookie that is sent to browser
        # browser sends back with subsequent requests
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    # now user id is stored in session it will be available on subsequent requests
    # at beginning of each request if a user is logged in their info should be loaded and made available to other views
    return render_template('auth/login.html')

# to logout, need to remove user id from session
# then load_logged_in_user wont load user on subsequent request
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#creating, editing and deleting blog posts require use to be logged in
# decorator used to check this for each view its applied
def login_required(view):
    # **kwargs is magic variable allows you to pass keyworded variable length of arguments to function
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
# decorator returns a new view function that wraps original view its applied to
# new function checks if user is loaded and redirects to login page otherwise
# if user is loaded original view is called and continues normally
    """