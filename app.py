from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_compress import Compress
from flask_cache import Cache
from flask_sslify import SSLify
from flask_login import LoginManager
from ago import human
import os

app = Flask(__name__)
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
Markdown(app)
if 'ON_HEROKU' in os.environ:
    sslify = SSLify(app)

# noinspection PyPep8
from views import *
# noinspection PyPep8
from models import *

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object('config')

Compress(app)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.context_processor
def inject_categories():
    query = db.session.query(Projects.category.distinct().label("category"))
    g.categories = [row.category for row in query.all()]
    return dict(categories=g.categories)


@app.context_processor
def inject_python():
    return dict(enumerate=enumerate, list=list, len=len, human=human, sum=sum)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # loop = asyncio.get_event_loop()
    app.run(host='0.0.0.0', port=port, debug=False)
    # loop.run_in_executor(None, functools.partial(app.run, host='0.0.0.0', port=port, debug=True))
    # loop.run_until_complete(run_discord())
