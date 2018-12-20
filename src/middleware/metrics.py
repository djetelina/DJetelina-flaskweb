import contextvars
import time

from prometheus_client import Histogram
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse

time_start = contextvars.ContextVar('time_start')
request_duration_s = Histogram(
    "request_duration_seconds", "Time spent processing requests",
    labelnames=["app", "method", "endpoint", "status_code"]
)


class MetricsMiddleware:
    def __init__(self, app: Sanic) -> None:
        self.app = app
        self.app.register_middleware(self.before_request, attach_to='request')
        self.app.register_middleware(self.after_request, attach_to='response')

    async def before_request(self, request: Request) -> None:
        time_start.set(time.time())

    async def after_request(self, request: Request, response: HTTPResponse) -> None:
        time_spent = time.time() - time_start.get()
        request_duration_s.labels(
            app=self.app.name, method=request.method, endpoint=request.path, status_code=response.status
        ).observe(time_spent)
