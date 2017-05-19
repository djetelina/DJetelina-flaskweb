from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_compress import Compress
from flask_cache import Cache
from flask_sslify import SSLify
from flask_login import LoginManager
from ago import human
import os

from plugins.runescape import blueprint as rs
import rses.rses.src as rses

app = Flask(__name__)
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
Markdown(app, safe_mode=False)
if 'ON_HEROKU' in os.environ:
    sslify = SSLify(app)
    debug = False
else:
    debug = True

# noinspection PyPep8
from views import *
# noinspection PyPep8
from models import *

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object('config')

Compress(app)
app.register_blueprint(rs.rs_bp)
app.register_blueprint(rses.rses_api_bp)
app.register_blueprint(rses.rses_web_client_bp)


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
    app.run(host='0.0.0.0', port=port, debug=debug)
    # loop.run_in_executor(None, functools.partial(app.run, host='0.0.0.0', port=port, debug=True))
    # loop.run_until_complete(run_discord())
