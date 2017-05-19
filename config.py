import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('FLASK_KEY')
if 'ON_HEROKU' in os.environ:
    RECAPTCHA_USE_SSL = True
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET')
RECAPTCHA_PUBLIC_KEY = "6LccjiQTAAAAAEwdsidF6K9zRkESbxbAoi0hvC_A"
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
