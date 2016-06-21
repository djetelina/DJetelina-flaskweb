import os
from app import app, db
from flask import render_template, send_from_directory, request, flash, session, redirect, url_for
from models import Projects
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', projects = Projects.query.all())


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != os.environ.get('password'):
            flash('Incorrect password')
        else:
            session['logged_in'] = True
            flash('Logged in')
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


@app.route("/add_project", methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['category'] or not request.form['info']:
            flash('Please fill Name, Category and Info', 'error')
        else:
            project = Projects(request.form['name'], request.form['category'], request.form['info'],
                               github=request.form['github'])
            db.session.add(project)
            db.session.commit()
            flash('New project added')

    return render_template('new.html')