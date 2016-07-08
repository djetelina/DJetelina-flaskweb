import os
from app import app, db, cache, recaptcha
from flask import render_template, send_from_directory, request, flash, session, redirect, url_for, make_response, g
from models import Projects
from forms import ProjectForm
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
    projects = Projects.query.order_by(Projects.modified.desc()).limit(3).all()
    return render_template('home.html', projects=projects)


@app.route("/admin/")
@login_required
def admin():
    return render_template('admin.html', projects=Projects.query.order_by(Projects.created.desc()).all())


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] != os.environ.get('password'):
            flash('Incorrect password')
        elif recaptcha.verify():
            session['logged_in'] = True
            flash('Logged in')
            return redirect(url_for('admin'))
        else:
            flash("Don't bypass ReCaptcha!")
    return render_template('login.html', captcha=recaptcha.get_code())


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
    found = Projects.query.filter(Projects.slug == project_name).first()
    if found:
        return render_template('project.html',
                               project=found)
    else:
        return render_template('404.html'), 404


@app.route("/edit/<string:name>/", methods=['GET', 'POST'])
@login_required
def edit(name):
    form = ProjectForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            selected_project = Projects.query.filter(Projects.slug == name).first()
            selected_project.name = form.name.data
            selected_project.category = form.category.data
            selected_project.info = form.info.data
            selected_project.slug = form.slug.data
            selected_project.status = form.status.data
            if form.url.data:
                selected_project.url = form.url.data
            else:
                selected_project.url = None
            if form.github.data:
                selected_project.github = form.github.data
            else:
                selected_project.github = None
            db.session.commit()
            flash('Project edited')
        else:
            flash('Validation error')
    return render_template('edit.html',
                           project=Projects.query.filter(Projects.slug == name).first(),
                           form=form)


@app.route("/delete/<string:name>/")
@login_required
def delete(name):
    selected_project = Projects.query.filter(Projects.slug == name).first()
    db.session.delete(selected_project)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/add_project/", methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_project = Projects(form.name.data, form.category.data, form.info.data, form.slug.data,
                                   form.status.data, github=form.github.data, url=form.url.data)
            db.session.add(new_project)
            db.session.commit()
            flash('New project added')
        else:
            flash('Validation failed')

    return render_template('new.html', form=form)


@app.route("/sitemap.xml")
def sitemap():
    projects = Projects.query.order_by(Projects.created.desc()).all()

    query = db.session.query(Projects.category.distinct().label("category"))
    categories = [row.category for row in query.all()]

    pages = []
    filter_rule = ["/sitemap.xml", "/robots.txt", "/login/", "/logout/", "/admin/", "/add_project/", "/favicon.ico"]
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0 and rule.rule not in filter_rule:
            pages.append(rule.rule)

    sitemap_xml = render_template('sitemap_template.xml', pages=pages, projects=projects, categories=categories)
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
