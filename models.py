from app import db


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64))
    github = db.Column(db.String(250))
    url = db.Column(db.String(250))
    info = db.Column(db.String(5000))
    status = db.Column(db.String(64))
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
