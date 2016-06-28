import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('FLASK_KEY')
