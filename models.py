from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from plugins.github import Commits


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64))
    github = db.Column(db.String(250))
    url = db.Column(db.String(250))
    info = db.Column(db.String(5000))
    status = db.Column(db.String(64))
    tags = db.Column(db.String(500))
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    modified = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name, category, info, slug, status, github=None, url=None):
        self.name = name
        self.category = category
        self.info = info
        self.slug = slug
        self.status = status
        if github is not None:
            self.github = github
        if url is not None:
            self.url = url

    def update(self, form):
            self.name = form.name.data
            self.category = form.category.data
            self.info = form.info.data
            self.slug = form.slug.data
            self.status = form.status.data
            self.tags = form.tags.data
            if form.url.data:
                self.url = form.url.data
            else:
                self.url = None
            if form.github.data:
                self.github = form.github.data
            else:
                self.github = None

    def get_tags(self):
        return self.tags.replace(" ", "").split(",")


    @property
    def commits(self):
        return Commits(self.github)



class User(db.Model):
    email = db.Column(db.String(64), primary_key=True, unique=True)
    hash = db.Column(db.String(300))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        self.email = email
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
