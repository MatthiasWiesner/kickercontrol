import os
from flask import (Flask,
                   render_template,
                   request,redirect,
                   url_for, flash,
                   session,
                   send_from_directory)
from flask.ext.login import (LoginManager,
                             login_user,
                             logout_user,
                             current_user,
                             login_required)
from .model import User, Game, init_engine, db_session
from .forms import LoginForm, SignupForm, GameForm
from .auth import (authorized,
                   require,
                   IsUser,
                   Any,
                   login_serializer)
from itsdangerous import constant_time_compare, BadData
from hashlib import sha1
from . import config

app = Flask(__name__)
app.config.from_object(config)
app.jinja_env.globals['authorized'] = authorized

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

init_engine(app.config['DB_URI'])

from . import kickit


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.jinja')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            if form.password.data == form.password_confirm.data:
                user = User(username=form.username.data, email=form.email.data, password=form.password.data)
                db_session.add(user)
                db_session.commit()
                if login_user(user, remember=form.remember.data):
                    # Enable session expiration only if user hasn't chosen to be
                    # remembered.
                    session.permanent = not form.remember.data
                    flash('Logged in successfully!', 'success')
                    return redirect(request.args.get('next') or url_for('index'))
                else:
                    flash('This email is disabled!', 'error')
            else:
                flash('Wrong password!', 'error')
        else:
            flash('User already exists!', 'error')
    return render_template('signup.jinja', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.valid_password(form.password.data):
            if login_user(user, remember=form.remember.data):
                # Enable session expiration only if user hasn't chosen to be
                # remembered.
                session.permanent = not form.remember.data
                flash('Logged in successfully!', 'success')
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('This username is disabled!', 'error')
        else:
            flash('Wrong username or password!', 'error')
    return render_template('login.jinja', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.token_loader
def load_token(token):
    try:
        max_age = app.config['REMEMBER_COOKIE_DURATION'].total_seconds()
        user_id, hash_a = login_serializer.loads(token, max_age=max_age)
    except BadData:
        return None
    user = User.query.get(user_id)
    if user is not None:
        hash_a = hash_a.encode('utf-8')
        hash_b = sha1(user.password).hexdigest()
        if constant_time_compare(hash_a, hash_b):
            return user
    return None


@app.teardown_request
def remove_db_session(exception=None):
    db_session.remove()


@app.errorhandler(403)
def forbidden_403(exception):
    return render_template('forbidden.jinja'), 403
