import os
from app import app, db, cache
from flask import render_template, send_from_directory, request, flash, session, redirect, url_for, make_response
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
@app.route("/home/")
@cache.cached(timeout=50)
def home():
    return render_template('home.html')


@app.route("/admin/")
@login_required
def admin():
    return render_template('admin.html', projects=Projects.query.order_by(Projects.created.desc()).all())


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] != os.environ.get('password'):
            flash('Incorrect password')
        else:
            session['logged_in'] = True
            flash('Logged in')
            return redirect(url_for('admin'))
    return render_template('login.html')


@app.route("/logout/")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


@app.route("/about/")
@cache.cached(timeout=50)
def about():
    return render_template('about.html')


@app.route("/projects/<string:category_name>/")
def category(category_name):
    found = Projects.query.filter(Projects.category == category_name).order_by(Projects.created.desc()).all()
    if found:
        return render_template('projects.html',
                               category=category_name,
                               projects=found,
                               )
    else:
        return render_template('404.html'), 404


@app.route("/projects/")
def projects():
    return render_template('projects.html',
                           projects=Projects.query.order_by(Projects.created.desc()).all())


@app.route("/project/<string:project_name>/")
def project(project_name):
    found = Projects.query.filter(Projects.name == project_name).first()
    if found:
        return render_template('project.html',
                               project=found)
    else:
        return render_template('404.html'), 404


@app.route("/edit/<string:name>/", methods=['GET', 'POST'])
@login_required
def edit(name):
    if request.method == 'POST':
        if not request.form['name'] or not request.form['category'] or not request.form['info']:
            flash('Please fill Name, Category and Info', 'error')
        else:
            selected_project = Projects.query.filter(Projects.name == name).first()
            selected_project.name = request.form['name']
            selected_project.category = request.form['category']
            selected_project.info = request.form['info']
            selected_project.slug = request.form['slug']
            selected_project.status = request.form['status']
            if request.form['url']:
                selected_project.url = request.form['url']
            else:
                selected_project.url = None
            if request.form['github']:
                selected_project.github = request.form['github']
            else:
                selected_project.github = None
            db.session.commit()
            flash('Project edited')
    return render_template('edit.html',
                           project=Projects.query.filter(Projects.name == name).first())


@app.route("/delete/<string:name>/")
@login_required
def delete(name):
    selected_project = Projects.query.filter(Projects.name == name).first()
    db.session.delete(selected_project)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/add_project/", methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['category'] or not request.form['info']:
            flash('Please fill Name, Category and Info', 'error')
        else:
            new_project = Projects(request.form['name'], request.form['category'], request.form['info'],
                                   request.form['slug'], request.form['status'],
                                   github=request.form['github'], url=request.form['url'])
            db.session.add(new_project)
            db.session.commit()
            flash('New project added')

    return render_template('new.html')


@app.route("/sitemap.xml")
def sitemap():
    pages = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(rule.rule)

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')


@app.route("/.well-known/acme-challenge/<string:file>")
def ssl_verif(file):
    if file == "zBoZTgJhuUvbAx2d2bSOzLbAxU5vQRG-y_aLx3-7Buk":
        return "zBoZTgJhuUvbAx2d2bSOzLbAxU5vQRG-y_aLx3-7Buk.zD-PdGHKwLK8VwOuRsL2KKdJ5VcSCYQqeXbYUXHmLog"
    elif file == "X3S6SqAQRClyntXga8IXKyh5U3WlAWyx8u-rDvFzdo0":
        return "X3S6SqAQRClyntXga8IXKyh5U3WlAWyx8u-rDvFzdo0.zD-PdGHKwLK8VwOuRsL2KKdJ5VcSCYQqeXbYUXHmLog"
