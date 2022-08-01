from flask import redirect, render_template, url_for, request, abort
from app import app
from app.modules.stats import Player
from app.modules.forms import SearchPlayer
import pickle




@app.route('/<server>/<username>', methods=['GET','POST'])
def stats(server, username):
    player_stats = Player(username, server)
    if player_stats.error == 429:
        abort(429)
    elif player_stats.error == 404:
        abort(404)

    form = SearchPlayer()
    if request.method == 'POST':
        if form.validate_on_submit() and form.server.data:
            server = form.server.data
            username = form.username.data
            return redirect(url_for('stats', server=server, username=username))

        elif 'refresh' in request.form:
            player_stats.get_data(username, server)
            return redirect(url_for('stats', server=server, username=username))


    return render_template('stats.html.jinja2', profile=player_stats, stats=player_stats.matches_list, form=form)

@app.route('/', methods=['GET','POST'])
def index():
    form = SearchPlayer()
    if form.validate_on_submit():
        server = form.server.data
        username = form.username.data
        return redirect(url_for('stats', server=server, username=username))
    return render_template('index.html.jinja2', form=form)


@app.errorhandler(404)
def user_not_found(e):
    form = SearchPlayer()
    if form.validate_on_submit():
        server = form.server.data
        username = form.username.data
        return redirect(url_for('stats', server=server, username=username))
    return render_template('404.html.jinja2', form=form), 404

@app.errorhandler(429)
def too_many_requests(e):
    form = SearchPlayer()
    if form.validate_on_submit():
        server = form.server.data
        username = form.username.data
        return redirect(url_for('stats', server=server, username=username))
    return render_template('429.html.jinja2', form=form), 429