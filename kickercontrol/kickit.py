from kickercontrol import app
from flask import render_template, request, redirect, url_for, flash
from .model import User, Game, db_session
from .forms import GameForm
from flask.ext.login import login_required


@app.route('/stats')
@login_required
def stats():
    games = Game.query.all()
    players = {}
    for g in games:
        for uid in [g.teamBlack_backend, g.teamBlack_frontend, g.teamRed_backend, g.teamRed_frontend]:
            if uid not in players:
                players[uid] = {'username': User.query.get(uid).username, 'score': 0, 'received': 0, 'won': 0, 'total': 0}

        players[g.teamBlack_backend]['total'] += 1
        players[g.teamBlack_frontend]['total'] += 1
        players[g.teamRed_backend]['total'] += 1
        players[g.teamRed_frontend]['total'] += 1

        if g.teamBlack_result > g.teamRed_result:
            players[g.teamBlack_backend]['won'] += 1
            players[g.teamBlack_frontend]['won'] += 1
        else:
            players[g.teamRed_backend]['won'] += 1
            players[g.teamRed_frontend]['won'] += 1

        players[g.teamBlack_backend]['score'] += g.teamBlack_result
        players[g.teamBlack_frontend]['score'] += g.teamBlack_result
        players[g.teamRed_backend]['score'] += g.teamRed_result
        players[g.teamRed_frontend]['score'] += g.teamRed_result
        
        players[g.teamBlack_backend]['received'] += g.teamRed_result
        players[g.teamBlack_frontend]['received'] += g.teamRed_result
        players[g.teamRed_backend]['received'] += g.teamBlack_result
        players[g.teamRed_frontend]['received'] += g.teamBlack_result

    order = str(request.args.get('order', 'score'))
    reverse = bool(request.args.get('reverse', 'False'))
    print reverse

    players = sorted(players.values(), key=lambda x: x[order], reverse=reverse)
    return render_template('stats.jinja', players=players)


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    form = GameForm()
    users = [[u.id, u.username] for u in User.query.all()]
    form.teamBlack_frontend.choices = users
    form.teamBlack_backend.choices = users
    form.teamRed_frontend.choices = users
    form.teamRed_backend.choices = users

    if form.validate_on_submit():
        if len(set([int(form.teamBlack_frontend.data),
                int(form.teamBlack_backend.data),
                int(form.teamRed_frontend.data),
                int(form.teamRed_backend.data)])) < 4:
            flash('Doubled player!', 'error')
            return render_template('game.jinja', form=form)

        if int(form.teamBlack_result.data) < 10 \
            and int(form.teamRed_result.data) < 10:
            flash('No winner!', 'error')
            return render_template('game.jinja', form=form)

        if int(form.teamBlack_result.data) == 10 \
            and int(form.teamRed_result.data) == 10:
            flash('Only one team wins!', 'error')
            return render_template('game.jinja', form=form)

        game = Game(teamBlack_result=int(form.teamBlack_result.data),
                    teamRed_result=int(form.teamRed_result.data),
                    teamBlack_frontend=int(form.teamBlack_frontend.data),
                    teamBlack_backend=int(form.teamBlack_backend.data),
                    teamRed_frontend=int(form.teamRed_frontend.data),
                    teamRed_backend=int(form.teamRed_backend.data))
        db_session.add(game)
        db_session.commit()
        flash('Game saved!', 'success')
    return render_template('game.jinja', form=form, users=users)


@app.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    Game.query.delete()
    db_session.commit()
    flash('Game table resetted!', 'success')
    return redirect(url_for('game'))
