import logging
import os

from blueprints.system import system_bp
from middleware.metrics import MetricsMiddleware

from raven.conf import setup_logging as add_sentry_handler
from raven.handlers.logging import SentryHandler
from sanic import Sanic


app = Sanic(name='djetelina.cz')

if os.getenv('DJETELINA_SENTRY_URL'):
    sentry_handler = SentryHandler(os.environ['DJETELINA_SENTRY_URL'])
    sentry_handler.setLevel(logging.ERROR)
    add_sentry_handler(sentry_handler)

MetricsMiddleware(app).register()
app.blueprint(system_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
