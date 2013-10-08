import os
from datetime import timedelta

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

from .model import (User,
                    Game,
                    init_engine,
                    db_session,
                    add_user,
                    add_game)

from .forms import (LoginForm,
                    SignupForm,
                    GameForm)

from .auth import (authorized,
                   require,
                   IsUser,
                   Any)

DB_URI = 'sqlite:///users.db'
DEBUG = True
SECRET_KEY = 'foobarbaz'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.globals['authorized'] = authorized

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

init_engine(app.config['DB_URI'])


@app.errorhandler(403)
def forbidden_403(exception):
    return render_template('forbidden.jinja'), 403


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.jinja')


@app.route('/stats')
@login_required
def stats():
    games = Game.query.all()
    players = {}
    for g in games:
        for uid in [g.teamA_backend, g.teamA_frontend, g.teamB_backend, g.teamB_frontend]:
            if uid not in players:
                players[uid] = {'username': User.query.get(uid).username, 'score': 0, 'won': 0, 'total': 0}

        players[g.teamA_backend]['total'] += 1
        players[g.teamA_frontend]['total'] += 1
        players[g.teamB_backend]['total'] += 1
        players[g.teamB_frontend]['total'] += 1

        if g.teamA_result > g.teamB_result:
            players[g.teamA_backend]['won'] += 1
            players[g.teamA_frontend]['score'] += 1
        else:
            players[g.teamB_backend]['won'] += 1
            players[g.teamB_frontend]['score'] += 1

        players[g.teamA_backend]['score'] += g.teamA_result
        players[g.teamA_frontend]['score'] += g.teamA_result
        players[g.teamB_backend]['score'] += g.teamB_result
        players[g.teamB_frontend]['score'] += g.teamB_result

    players = sorted(players.items(), key=lambda x: x[1])
    players.reverse()
    return render_template('stats.jinja', players=players)


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    form = GameForm()

    users = [[u.id, u.username] for u in User.query.all()]
    form.teamA_frontend.choices = users
    form.teamA_backend.choices = users
    form.teamB_frontend.choices = users
    form.teamB_backend.choices = users

    if form.validate_on_submit():
        if len(set([int(form.teamA_frontend.data),
                int(form.teamA_backend.data),
                int(form.teamB_frontend.data),
                int(form.teamB_backend.data)])) < 4:
            flash('Doubled player!', 'error')

        add_game(int(form.teamA_result.data),
            int(form.teamB_result.data),
            int(form.teamA_frontend.data),
            int(form.teamA_backend.data),
            int(form.teamB_frontend.data),
            int(form.teamB_backend.data))

    return render_template('game.jinja', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            if form.password.data == form.password_confirm.data:
                user = add_user(form.username.data, form.email.data, form.password.data)
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


@app.teardown_request
def remove_db_session(exception=None):
    db_session.remove()
