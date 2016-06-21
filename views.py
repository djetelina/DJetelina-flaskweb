import os
from run import app, db
from flask import render_template, send_from_directory, request, flash
from models import Projects


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html', projects = Projects.query.all())

@app.route("/add_project", methods = ['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['category'] or not request.form['info']:
            flash('Please enter all the fields', 'error')
        else:
            project = Projects(request.form['name'], request.form['category'], request.form['info'],
                               github=request.form['github'])
            db.session.add(project)
            db.session.commit()

            flash('New project added')
    return render_template('new.html')