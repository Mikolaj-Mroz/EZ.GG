from flask import redirect, render_template, url_for, request
from app import app
from app.modules.stats import Player
from app.modules.forms import SearchPlayer, Refresh
import pickle




@app.route('/<server>/<username>', methods=['GET','POST'])
def stats(server, username):
    player_stats = Player(username, server)
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