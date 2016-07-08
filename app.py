from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_compress import Compress
from flask_cache import Cache
from flask_sslify import SSLify
from flask_recaptcha import ReCaptcha
from ago import human
import os

app = Flask(__name__)
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
Markdown(app)
recaptcha = ReCaptcha(site_key=os.environ.get('RECAPTCHA_SITE'), secret_key=os.environ.get("RECAPTCHA_SECRET"), theme='dark')
recaptcha.init_app(app)
if 'ON_HEROKU' in os.environ:
    sslify = SSLify(app)

from views import *
from models import *

app.config.from_object('config')

Compress(app)

@app.context_processor
def inject_categories():
    query = db.session.query(Projects.category.distinct().label("category"))
    g.categories = [row.category for row in query.all()]
    return dict(categories=g.categories)

@app.context_processor
def inject_python():
    return dict(enumerate=enumerate, list=list, len=len, human=human)

if __name__ == "__main__":
    db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
